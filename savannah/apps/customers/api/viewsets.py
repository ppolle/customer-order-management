from rest_framework import viewsets
from savannah.apps.customers.models import Customer
from savannah.apps.customers.api.serializers import CustomerSerializer

class CustomerViewsets(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
