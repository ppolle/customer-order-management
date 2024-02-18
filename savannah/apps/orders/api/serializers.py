from rest_framework import serializers
from savannah.apps.orders.models import Order

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_number', 'time')