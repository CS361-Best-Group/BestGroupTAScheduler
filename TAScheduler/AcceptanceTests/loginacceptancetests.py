from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# As a user, I must be able to log into my account, in order to use the system.
class TestLoginAcceptance(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.userA = User.objects.create_user('jsmith', 'jsmith@example.edu', '123')
        self.userB = User.objects.create_user('awest', 'awest@example.edu', '321')
    
    def testValid(self):
        # WHEN I submit a set of credentials.
        response = self.client.post('/login/', {'name': 'jsmith', 'password': '123'}, follow = True)
        # THEN the credentials are validated by the system.
        
        # WHEN the credentials are valid and authorized for use with this system.
        # THEN my browser navigates past the login prompt to the system proper.
        self.assertRedirects(response, '/')
        self.assertEqual(response.wsgi_request.user, self.userA)
    
    def testInvalid(self):
        # WHEN I submit a set of credentials.
        response = self.client.post('/login/', {'name': 'jsmith', 'password': '321'}, follow = True)
        # THEN the credentials are validated by the system.
        
        # WHEN the credentials are invalid.
        # THEN my browser navigates back to the login prompt.
        # AND I am informed that my credentials are invalid.
        self.assertEqual(response.context.request.path, '/login/')
        self.assertNotEqual(response.wsgi_request.user, self.userA)
