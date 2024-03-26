from django.urls import path
from .viewsets import AuthenticateView, CallbackView

urlpatterns = [
    path('authenticate/', AuthenticateView.as_view()),
    path('callback/', CallbackView.as_view()),
]
