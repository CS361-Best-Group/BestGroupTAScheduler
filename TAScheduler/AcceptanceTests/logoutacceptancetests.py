from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# As a user, I must be able to log out of my account, in order to ensure my account is not used by someone else.
class TestLogoutAcceptance(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.userA = User.objects.create_user("jsmith", "jsmith@example.edu", "123")
        self.userB = User.objects.create_user("awest", "awest@example.edu", "321")
        
        # GIVEN I am currently logged into my account.
        self.client.force_login(self.userA)
    
    def testLogout(self):
        # WHEN I press the 'log out' button.
        response = self.client.get("/login/", follow = True)
        
        # THEN my session is ended.
        self.assertNotEqual(response.wsgi_request.user, self.userA)
        # AND I am returned to the login prompt.
        self.assertEqual(response.context.request.path, "/login/")
