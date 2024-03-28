from django.test import TestCase
from rest_framework.test import APIClient
from savannah.apps.orders.models import Order
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from savannah.apps.customers.models import Customer
from savannah.apps.notifications.models import Notification

User = get_user_model()
# Create your tests here.

class OrderApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@gmail.com',
            password='testPASSWORD1234')
        self.token, created = Token.objects.get_or_create(user=self.user)

        self.customer = Customer.objects.create(name="John Doe",
                                                user=self.user)
        self.order = Order.objects.create(customer=self.customer,
                                          item="Fancy Watch",
                                          amount= 4)
        

        self.client = APIClient()

    def test_order_object_creation(self):
        url = '/api/v1/orders/'
        data = {'customer': self.customer.id,
                'item': 'Sued Shoes',
                'amount':2}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.all().count(), 2)
        self.assertEqual(response.data['item'], 'Sued Shoes')

    def test_notification_object_creation(self):
        notification_count = Notification.objects.all().count()

        url = '/api/v1/orders/'
        data = {'customer': self.customer.id,
                'item': 'Jeans',
                'amount': 1}
        
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))
        order = Order.objects.get(id=response.data['id'])
        updated_notification_count = Notification.objects.all().count()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(notification_count+1,updated_notification_count)
        self.assertTrue(Notification.objects.get(order=order))

    def test_order_object_patch(self):
        url = f'/api/v1/orders/{self.order.id}/'
        data = {'amount': 3}
        response = self.client.patch(
            url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], 3)

    def test_order_object_put(self):
        url = f'/api/v1/orders/{self.order.id}/'
        data = {'amount': 2,
                'customer': self.customer.id,
                'item':'Sued Shoes'}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], 2)

    def test_order_object_deletion(self):
        url = f'/api/v1/orders/{self.order.id}/'
        response = self.client.delete(
            url, HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 204)

    def test_order_code_creation(self):
        url = '/api/v1/orders/'
        data = {'customer': self.customer.id,
                'item': 'Taste Afrique',
                'amount': 5}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 201)
        self.assertIn('#ON', response.data['order_number'])

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@gmail.com',
            password='testPASSWORD1234')
        
        self.customer = Customer.objects.create(name="John Doe",
                                                user=self.user)       


    def test_order_model_str(self):
        order = Order.objects.create(customer=self.customer,
                                         item="White trouser",
                                         amount=1)
        self.assertTrue(isinstance(order, Order))

        self.assertEqual(order.__str__(), f'{order.order_number} - {self.customer.name}')
