from django.http import Http404
from rest_framework import status
from django.shortcuts import redirect
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError
from savannah.apps.users.authentication import GoogleAuth
from rest_framework import viewsets, permissions, authentication

User = get_user_model()

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
    
class UserViewSet(APIView):
    """
    Get and Update User Data
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutViewSet(APIView):
    """
    Get and Update User Data
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        Token.objects.get(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
