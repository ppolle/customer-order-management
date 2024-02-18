from rest_framework import viewsets
from savannah.apps.orders.models import Order
from savannah.apps.orders.api.serializers import OrderSerializers

class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
