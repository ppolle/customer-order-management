from django.urls import path
from .viewsets import AuthenticateView, CallbackView, UserViewSet, LogoutViewSet

urlpatterns = [
    path('user/', UserViewSet.as_view()),
    path('logout/', LogoutViewSet.as_view()),
    path('authenticate/', AuthenticateView.as_view()),
    path('callback/', CallbackView.as_view()),
]
