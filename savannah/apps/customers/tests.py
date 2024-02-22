from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from savannah.apps.customers.models import Customer

# Create your tests here.

class CustomerApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@gmail.com',
            password='testPASSWORD1234')
        
        self.customer = Customer.objects.create(name="John Doe",
                                                user=self.user)

        self.client = APIClient()

    def test_customer_object_creation(self):
        url = '/api/v1/customers/'
        data = {'user':self.user.id,
				'name':'John Doe'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.all().count(), 2)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.status_code, 201)
    def test_customer_object_patch(self):
        url = f'/api/v1/customers/{self.customer.id}/'
        data = {'name': 'Jane Doe'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Jane Doe')

    def test_customer_object_put(self):
        url = f'/api/v1/customers/{self.customer.id}/'
        data = {'name': 'Pinky Ponky',
                'user':self.user.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Pinky Ponky')

    def test_customer_object_deletion(self):
        url = f'/api/v1/customers/{self.customer.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_customer_code_creation(self):
        url = '/api/v1/customers/'
        data = {'user': self.user.id,
                'name': 'John Doe'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('#CU', response.data['customer_code'])

class CustomerModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@gmail.com',
            password='testPASSWORD1234')

        self.customer = Customer.objects.create(name="Bob Marley",
                                                user=self.user)

    def test_customer_model_str(self):
        customer1 = Customer.objects.create(name="Jakaya Kikwete",
                                            user=self.user)
        self.assertTrue(isinstance(customer1, Customer))
        self.assertEqual(customer1.__str__(), customer1.name)

