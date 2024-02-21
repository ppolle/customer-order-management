from django.db import models
from savannah.apps.customers.models import Customer
# Create your models here.

class Order(models.Model):
    """
    Customer orders
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, null=True, blank=True)
    item = models.CharField(max_length=255)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"
    
    def save(self, *args, **kwargs):
        super(Order, self).save()
        order_number = f"#ON{self.id}"
        self.order_number = order_number

