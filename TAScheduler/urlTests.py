from django.test import TestCase
from django.test import Client



class TestUrls(TestCase):
    def setUp(self):
        self.client=Client()


 #    def test_adminURL(self):
 #
 #       r=self.client.post('/admin/', {"username":"blah", "password":"blah"})
 #       print(r.url)
 #       self.assertEqual(r.url, "/admin/")
    def test_loginTemplates(self):
        r = self.client.get("/login/")
        self.assertEqual(r.templates[0].name, "login.html")

    def test_courseCreationTemplates(self):
        r = self.client.get("/coursecreation/")
        self.assertEqual(r.templates[0].name, "coursecreation.html")

    def test_accountCreationTemplates(self):
        r = self.client.get("/accountcreation/")
        self.assertEqual(r.templates[0].name,  "accountcreation.html")

    def test_loginPath(self):
        r=self.client.get("/login/")
        self.assertEqual(r.context.request.path, "/login/")

    def test_courseCreationPath(self):
        r=self.client.get("/coursecreation/")
        self.assertEqual(r.context.request.path, "/coursecreation/")

    def test_accountCreationPath(self):
        r=self.client.get("/accountcreation/")
        self.assertEqual(r.context.request.path, "/accountcreation/")

