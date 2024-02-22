from django.db import models
from django.dispatch import receiver
from savannah.apps.orders.models import Order
from django.db.models.signals import post_save
from savannah.apps.notifications.notifications import SendSMS

# Create your models here.
class Notification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.status}'

@receiver(post_save, sender=Order)
def create_notification(sender, instance, created, **kwargs):
    if created:
        sms = SendSMS(instance)
        response = sms.send()
        response_data = response['SMSMessageData']['Recipients'][0]
        Notification.objects.create(order=instance,
                                    status=response_data['status'],
                                    phone_number=response_data['number'],
                                    message_id=response_data['messageId'])
        

{'SMSMessageData': {'Message': 'Sent to 1/1 Total Cost: KES 0.8000 Message parts: 1',
                    'Recipients': [{'cost': 'KES 0.8000', 'messageId': 'ATXid_660c44371ac362e12eb7721416a0af98', 'number': '+254736492933', 'status': 'Success', 'statusCode': 101}]}}
