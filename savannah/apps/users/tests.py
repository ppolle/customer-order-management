from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from savannah.apps.customers.models import Customer
from savannah.apps.users.api.serializers import UserSerializer
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

    def test_retrieve_logged_in_user(self):
        url = '/api/v1/user/'
        response = self.client.get(
            url, HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        serializer = UserSerializer(self.user)
        
        self.assertEqual(serializer.data,response.data)

    def test_non_logged_in_user(self):
        url = '/api/v1/user/'
        response = self.client.get(url)

        serializer = UserSerializer(self.user)

        self.assertEqual(401, response.status_code)

    def test_partial_updates(self):
        url = '/api/v1/user/'
        response = self.client.patch(
            url, HTTP_AUTHORIZATION='Token ' + str(self.token), data={"phone_number":"+254736492933"})

        self.assertEqual("+254736492933", response.data['phone_number'])

    def test_non_partial_updates(self):
        url = '/api/v1/user/'
        payload = {
            "name": "real User",
            "email": "peter.m.polle@gmail.com",
            "phone_number": "",
            "profile_picture": "https://lh3.googleusercontent.com/a/ACg8ocJNcvmNYnBWNPd3AG28AS-7yFjcIRVdehiudeR5vcYT8G8=s96-c"
        }
        response = self.client.put(
            url, HTTP_AUTHORIZATION='Token ' + str(self.token), data=payload)

        serializer = UserSerializer(payload)

        self.assertEqual(serializer.data['name'], response.data['name'])

    def test_logout(self):
        url = '/api/v1/user/'
        response = self.client.get(
            url, HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(200, response.status_code)
        logout_url = '/api/v1/logout/'
        logout_response = self.client.get(
            logout_url, HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.assertEqual(logout_response.status_code, 204)

