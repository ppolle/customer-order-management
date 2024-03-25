from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from savannah.apps.users.api.serializers import SignupSerializer

User = get_user_model()

class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]
