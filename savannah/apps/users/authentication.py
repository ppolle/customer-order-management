import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

User = get_user_model()

class GoogleAuth:
    def __init__(self):
        self.GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
        self.SCOPES = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]

    def generate_client_config(self):
        # This follows the structure of the official "client_secret.json" file
        client_config = {"web": {"client_id": settings.GOOGLE_CLIENT_ID, 
                                 "project_id": settings.GOOGLE_PROJECT_ID, 
                                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                 "token_uri": "https://oauth2.googleapis.com/token", 
                                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", 
                                 "client_secret": settings.GOOGLE_CLIENT_SECRET, 
                                 "redirect_uris": settings.GOOGLE_AUTH_REDIRECT_URIS}
                                 }
        return client_config
    
    def generate_authorization_url(self):
        try:
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config=self.generate_client_config(),
                scopes=self.SCOPES,
                redirect_uri=settings.GOOGLE_AUTH_REDIRECT_URI)

            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent')
            
            return authorization_url, state
        except Exception as e:
            raise ValidationError(e)
    
    def get_user_info(self, access_token):
        response = requests.get(
                self.GOOGLE_USER_INFO_URL,
                params={'access_token': access_token}
            )                   

        if not response.ok:
            raise ValidationError('Failed to obtain user info from Google.')

        return response.json()

    def get_tokens(self, state, authorization_response):
        try:
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config=self.generate_client_config(),
                scopes=self.SCOPES,
                redirect_uri=settings.GOOGLE_AUTH_REDIRECT_URI,
                state=state
            )
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials

            return credentials
        except Exception as e:
            raise ValidationError(e)
        
    def user_data_to_dict(self, data):
        return {'name': data.name,
                'email':data.email,
                'picture':data.profile_picture}
    
    def authenticate_user(self, user_data):
        try:
            user = User.objects.get(email=user_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'user': self.user_data_to_dict(user),
                
            }
            return response_data
        except User.DoesNotExist:
            username = user_data['email'].split('@')[0]
            name = user_data.get('name', '')
 
            user = User.objects.create(
                username=username,
                email=user_data['email'],
                name=name,
                phone_number=None,
                profile_picture=user_data['picture']
            )
            
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'user': self.user_data_to_dict(user),
                
            }
            return response_data

        
        

