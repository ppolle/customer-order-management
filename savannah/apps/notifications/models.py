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
        if response['status'] == 'success':
            response_data = response['detail']['SMSMessageData']['Recipients'][0]
            Notification.objects.create(order=instance,
                                        status=response_data['status'],
                                        phone_number=response_data['number'],
                                        message_id=response_data['messageId'])