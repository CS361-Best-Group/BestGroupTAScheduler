from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group
from TAScheduler.apps import TASchedulerAppConfig
from TAScheduler.models import Profile

# As an administrator, I must be able to create accounts for the system, in order to allow new administrators, instructors and TAs to access the system.
class TestCourseCreationAcceptance(TestCase):
    def setUp(self):
        self.client = Client()
        
        TASchedulerAppConfig.ready(None)
        
        self.userA = User.objects.create_user('jsmith', 'jsmith@example.edu', '123')
        managerGroup = Group.objects.get(name = 'manager')
        
        # GIVEN my account has administrative privileges.
        managerGroup.user_set.add(self.userA)
        
        # AND I am currently logged into my account.
        self.client.force_login(self.userA)
    
    def testSuccessfulAccountCreation(self):
        # WHEN I submit a new account.
        response = self.client.post('/accountmanagement/', {'username': 'awest', 'password': '321', 'name': 'Adam West', 'email': 'awest@example.edu'}, follow = True)
        # THEN the account information is validated by the system.
        
        # WHEN the account information is valid.
        
        # THEN the account is added to the database.
        newUser = User.objects.get(username='awest')
        newProfile = Profile.objects.get(user=newUser)
        
        # AND I am redirected to the account management page, which displays the new course.
        self.assertEqual(response.context.request.path, '/accountmanagement/')
        self.assertTrue(newUser in response.context['Admin'])
        self.assertIn(newProfile, response.context['Profiles'])
    
    def testUnsuccessfulAccountCreation(self):
        accounts = User.objects.all()
        
        # WHEN I submit a new account.
        response = self.client.post('/accountmanagement/', {'username': '', 'password': '', 'name': '', 'email': ''}, follow = True)
        # THEN the account information is validated by the system.
        
        # WHEN the account information is invalid.
        
        # THEN I am redirected back to the account management page.
        # AND I am informed that the account information is invalid.
        self.assertEqual(response.context.request.path, '/accountmanagement/')
        self.assertEqual(list(response.context['Admin']), list(accounts))
