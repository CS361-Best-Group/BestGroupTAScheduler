from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from TAScheduler.models import Profile


class TestUrls(TestCase):
    def setUp(self):
        self.client=Client()
        
        self.User1 = User.objects.create_user(username="New Guy", password="testing", email="sethkinney6@gmail.com")
        self.User1.save()
        Profile1 = Profile(user=self.User1, address="9999", phone="111-111-1111", alt_email="alt@gmail.com")
        Profile1.save()

    def test_loginTemplates(self):
        self.client.force_login(self.User1)
        r = self.client.get("/login/")
        self.assertEqual(r.templates[0].name, "login.html")

    def test_courseCreationTemplates(self):
        self.client.force_login(self.User1)
        r = self.client.get("/coursemanagement/")
        self.assertEqual(r.templates[0].name, "coursemanagement.html")

    def test_accountCreationTemplates(self):
        self.client.force_login(self.User1)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.templates[0].name,  "usermanagement.html")

    def test_loginPath(self):
        r=self.client.get("/login/")
        self.assertEqual(r.context.request.path, "/login/")

    def test_courseCreationPath(self):
        self.client.force_login(self.User1)
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context.request.path, "/coursemanagement/")

    def test_accountCreationPath(self):
        self.client.force_login(self.User1)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context.request.path, "/accountmanagement/")

    def test_homeTemplate(self):
        self.client.force_login(self.User1)
        r=self.client.get("/")
        self.assertEqual(r.templates[0].name, "index.html")

    def test_profileTemplate(self):
        self.client.force_login(self.User1)
        r=self.client.get("/profile/")
        self.assertEqual(r.templates[0].name, "profile.html")

    def test_homePath(self):
        r=self.client.get("/", follow=True)
        self.assertRedirects(r, "/login/?next=/")

    def test_profilePath(self):
        self.client.force_login(self.User1)
        r=self.client.get("/profile/")
        self.assertEqual(r.context.request.path, "/profile/")
