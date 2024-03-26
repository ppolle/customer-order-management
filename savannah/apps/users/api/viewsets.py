from django.http import Http404
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
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
    pass
