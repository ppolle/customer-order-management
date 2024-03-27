import africastalking
from django.conf import settings

class SendSMS():
    def __init__(self, order):
       self.order = order
       self.username = settings.AT_USERNAME
       self.api_key = settings.AT_API_KEY
       self.sender= settings.AT_SENDER

    def initialize(self):

       africastalking.initialize(
            username=self.username,
            api_key=self.api_key
        )
       sms = africastalking.SMS
       
       return sms
    
    def send(self):
        sms = self.initialize()
        phone_number = self.order.customer.user.phone_number
        if phone_number is not None or phone_number != '':
         recipients = [phone_number] #swap this for actual user's phone number
         message = f"Hi {self.order.customer}, a new order has been placed on our platform. Order number is: {self.order.order_number}" #complete this
         sender = self.sender
         response = sms.send(message, recipients, sender)
         return {"status":"success","detail":response}

        return {"status":"fail"}

