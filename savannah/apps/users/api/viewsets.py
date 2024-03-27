from django.http import Http404
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from savannah.apps.users.authentication import GoogleAuth


class AuthenticateView(APIView):
    """
    Initialize Google oauth Authorization
    """
    def get(self, request, format=None):
        google_auth = GoogleAuth()
        authorization_url, state = google_auth.generate_authorization_url()
        request.session["google_oauth2_state"] = state

        return redirect(authorization_url)
        
class CallbackView(APIView):
    """
    Handle Google OAuth Callback 
    """
    def get(self, request, format=None):
        error = request.GET.get('error')
        if error:
            raise ValidationError({"status": "failed",
                                   "detail": error})
        
        google_auth = GoogleAuth()
        authorization_response=request.get_full_path()

        tokens = google_auth.get_tokens(
            state=request.GET.get('state'), authorization_response=authorization_response)
        
        user_info = google_auth.get_user_info(tokens.token)
        authenticate = google_auth.authenticate_user(user_info)

        return Response(authenticate)
