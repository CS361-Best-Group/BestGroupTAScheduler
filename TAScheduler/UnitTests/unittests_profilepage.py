import unittest

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test import Client
from ..models import Profile
from ..views import ProfilePage

# Test ProfilePage
class TestOtherProfile(unittest.TestCase):
    def setUp(self):
        #TASchedulerAppConfig.ready(None)
        self.user = User.objects.create_user('jsmith', 'jsmith@example.edu', '123')
        self.profile = Profile.objects.create(user=self.user, address='123 Main St. Anytown, USA', phone='555-123-4567', altemail='jsmith@example.edu')
        pass

    def test_changeName(self):
        ProfilePage.otherProfile(self.user, self.profile, { "name" : "new guy"})
        self.assertEqual(self.user.first_name, "new guy")
        pass

    def test_changeUserName(self):
        ProfilePage.otherProfile(self.user, self.profile, { "username" : "newUsername"})
        self.assertEqual(self.user.username, "newUsername")
        pass

    def test_changeEmail(self):
        ProfilePage.otherProfile(self.user, self.profile, { "email" : "new@guy.com"})
        self.assertEqual(self.user.username, "new@guy.com")
        pass

    def test_changeAddress(self):
        ProfilePage.otherProfile(self.user, self.profile, { "address" : "The Moon"})
        self.assertEqual(self.profile.username, "The Moon")
        pass

    def test_changePhone(self):
        ProfilePage.otherProfile(self.user, self.profile, { "phone" : "123-456-7890"})
        self.assertEqual(self.profile.phone, "123-456-7890")
        pass

    def test_changeAltemail(self):
        ProfilePage.otherProfile(self.user, self.profile, { "altemail" : "another@email.com"})
        self.assertEqual(self.profile.alt_email, "another@email.com")
        pass

class TestTAProfile(unittest.TestCase):
    def setUp(self):
        #TASchedulerAppConfig.ready(None)
        self.userTA = User.objects.create_user('jsmith', 'jsmith@example.edu', '123')
        self.profileTA = Profile.objects.create(user=self.userTA, address='123 Main St. Anytown, USA', phone='555-123-4567', altemail='jsmith@example.edu', skills="Really slow typer")

    def test_changeSkills(self):
        ProfilePage.otherProfile(self.user, self.profile, { "skills" : "Really fast typer"})
        self.assertEqual(self.profile.skills, "Really fast typer")
        pass