from savannah.apps.customers.models import Customer
from rest_framework import viewsets, authentication, permissions
from savannah.apps.customers.api.serializers import CustomerSerializer

class CustomerViewsets(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
