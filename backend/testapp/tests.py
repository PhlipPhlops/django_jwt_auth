from django.test import TestCase, Client
from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)

class EndpointTests(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create a test client
        self.client = Client()

    def test_test_endpoint(self):
        # Test the test_endpoint view
        response = self.client.get('/test_endpoint')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello from the backend!')

    def test_test_endpoint_auth(self):
        # Test the test_endpoint_auth view
        # Should return a 403 error, because the user is not authenticated
        response = self.client.get('/test_endpoint_auth')
        self.assertEqual(response.status_code, 401)

        # Authenticate the user
        self.login()

        # Test the test_endpoint_auth view again
        # Should return a 200 success response, because the user is now authenticated
        response = self.client.get('/test_endpoint_auth')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello from the backend! You are authenticated')

    def login(self):
        # Login the test user
        response = self.client.post('/login', {'username': self.username, 'password': self.password})
        # Extract the authentication token from the response
        auth_token = response.data['auth_token']
        # Set the HTTP_AUTHORIZATION header for the next request
        self.client = Client(HTTP_AUTHORIZATION='Token ' + auth_token)


    def test_login_user(self):
        # Test the login_user view
        response = self.client.post('/login', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

        # Extract the authentication token from the response
        auth_token = response.data['auth_token']

        # Set the HTTP_AUTHORIZATION header for the next request
        self.client = Client(HTTP_AUTHORIZATION='Token ' + auth_token)

        # Test the test_endpoint_auth view again
        response = self.client.get('/test_endpoint_auth')
        self.assertEqual(response.status_code, 200)


    def test_signup_user(self):
        # Test the signup_user view
        username = 'newuser'
        password = 'newpassword'
        response = self.client.post('/signup', {'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)

        # Test that the new user can be authenticated
        response = self.client.post('/login', {'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)


    def test_logout_user(self):
        # Test the logout_user view
        # Should return a 'Logout successful' response
        self.login()

        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 200)

