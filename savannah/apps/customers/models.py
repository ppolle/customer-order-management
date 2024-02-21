from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Customer(models.Model):
    """
    Customer's details
    """
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    customer_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Customer, self).save()
        customer_code = f"#CU{self.id}"
        self.customer_code = customer_code

    