import unittest
from django.test import TestCase
from django.test import Client
from .models import Profile

# Test Login
class LoginTest(TestCase):
    def setUp(self):
        user = Profile(name="a", password="test")
        user.save()
        self.client = Client()

    def test_RightPassword(self):
        self.request = self.client.post("", {"name": "a", "password": "test"}, follow=True)
        self.assertEqual(self.request.context["message"], "name password match", "the name and password do not match")

    def test_WrongPassword(self):
        self.request = self.client.post("", {"name": "a", "password": "wrongpassword"}, follow=True)
        self.assertEqual(self.request.context["message"], "bad password", "the name and password entered do not match")

    def test_NonexistantUser(self):
        self.request = self.client.post("", {"name": "b", "password": "b"}, follow=True)
        self.assertEqual(self.request.context["message"], "nonexistant user", "the name was not found")