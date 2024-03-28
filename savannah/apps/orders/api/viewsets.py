from savannah.apps.orders.models import Order
from rest_framework import viewsets, permissions, authentication
from savannah.apps.orders.api.serializers import OrderSerializers

class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
