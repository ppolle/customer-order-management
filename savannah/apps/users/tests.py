from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from savannah.apps.customers.models import Customer
from rest_framework.test import APIClient, APITestCase

User = get_user_model()

# Create your tests here.
class UserApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@gmail.com',
            password='testPASSWORD1234')
        self.token, created = Token.objects.get_or_create(user=self.user)

        self.customer = Customer.objects.create(name="John Doe",
                                                user=self.user)

        self.client = APIClient()

    def test_authenticate_redirection(self):
        url = '/api/v1/authenticate/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_user_creation_using_callback_api(self):
        url = '/api/v1/callback/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_user_creation_using_callback_api(self):
        pass
    