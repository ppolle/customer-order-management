import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.conf import settings


class GoogleAuth:

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
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=self.generate_client_config(),
            scopes=['profile', 'email'],
            redirect_uri=settings.GOOGLE_AUTH_REDIRECT_URIS[0])

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent')
        
        return authorization_url, state
    
    def get_user_info(self):
        pass

    def get_tokens(self, state, authorization_response):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=self.generate_client_config(),
            scopes=['profile', 'email'],
            redirect_uri=settings.GOOGLE_AUTH_REDIRECT_URIS[0],
            state=state
        )
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

        return credentials

        
        

