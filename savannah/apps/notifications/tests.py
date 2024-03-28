from django.test import TestCase
from .models import Notification
from savannah.apps.customers.models import Customer
from savannah.apps.orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.

class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@gmail.com',
            password='testPASSWORD1234')

        self.customer = Customer.objects.create(name="Bob Marley",
                                                user=self.user)
        self.order = Order.objects.create(customer=self.customer,
                                          item="Older TV",
                                          amount=2345)
    def test_customer_model_str(self):
        notification = Notification.objects.create(order=self.order,
                                                   status="success",
                                                   phone_number='+254736492933',
                                                   message_id="OWEOUWEW836")
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(notification.__str__(), f'{notification.phone_number} - {notification.status}')
