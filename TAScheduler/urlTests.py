from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Profile


class TestUrls(TestCase):
    def setUp(self):
        self.client=Client()

    def test_loginTemplates(self):
        r = self.client.get("/login/")
        self.assertEqual(r.templates[0].name, "login.html")

    def test_courseCreationTemplates(self):
        r = self.client.get("/coursemanagement/")
        self.assertEqual(r.templates[0].name, "coursemanagement.html")

    def test_accountCreationTemplates(self):
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.templates[0].name,  "usermanagement.html")

    def test_loginPath(self):
        r=self.client.get("/login/")
        self.assertEqual(r.context.request.path, "/login/")

    def test_courseCreationPath(self):
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context.request.path, "/coursemanagement/")

    def test_accountCreationPath(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context.request.path, "/accountmanagement/")

    def test_homeTemplate(self):
        User1=User.objects.create_user(username="seth", password="bruh")
        User1.save()
        session=self.client.session
        session["_auth_user_id"]=User1.id
        session.save()
        r=self.client.get("/")
        self.assertEqual(r.templates[0].name, "index.html")

    def test_profileTemplate(self):
        Users = User.objects.create_user(username="New Guy", password="testing", email="sethkinney6@gmail.com")
        Users.save()
        Profile1 = Profile(user=Users, address="9999", phone="111-111-1111", alt_email="alt@gmail.com")
        Profile1.save()
        mysession = self.client.session
        mysession['_auth_user_id'] = Users.id
        mysession.save()
        r=self.client.get("/profile/")
        self.assertEqual(r.templates[0].name, "profile.html")

    def test_homePath(self):
        r=self.client.get("/")
        self.assertRedirects("/login/")

    def test_profilePath(self):
        Users=User.objects.create_user(username="New Guy", password="testing", email="sethkinney6@gmail.com")
        Users.save()
        Profile1=Profile(user=Users, address="9999", phone="111-111-1111", alt_email="alt@gmail.com")
        Profile1.save()
        mysession=self.client.session
        mysession['_auth_user_id']=Users.id
        mysession.save()
        r=self.client.get("/profile/")
        self.assertEqual(r.context.request.path, "/profile/")