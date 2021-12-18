from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class TestLoginGet(TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user("username", "blah@gmail.com", "password")

        self.user.save()

        r = self.client.post("/login/", {"name": "username", "password": "password"}, follow=True)


    def test_getTemplate(self):
        r=self.client.get("/login/")
        self.assertEqual(r.templates[0].name, "login.html")


    def test_getsession(self):

        r=self.client.get("/login/")
        self.assertEqual(len(self.client.session.keys()),0)

    def test_getKeepLogin(self):
        user2=User.objects.create_user("Jimbo Jones", "jimbo@gmail.com", "jimbospassword")
        user2.save()
        client2=Client()
        client2.post("/login/", {"name":"Jimbo Jones", "password" :"jimbopassword"}, follow=True)

        client2.get("/login/")

        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.id)



class TestLoginPost(TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user("username", "blah@gmail.com", "password")

        self.user.save()

    def test_postGoodTemplate(self):
        r=self.client.post("/login/", {"name":"username", "password":"password"}, follow=True)
        self.assertEqual(r.templates[0].name, "index.html")

    def test_postGoodUrl(self):
        r=self.client.post("/login/", {"name":"username", "password":"password"}, follow=True)

        self.assertEqual(r.context.request.path, "/")
    def test_postGoodSession(self):

        r=self.client.post("/login/", {"name":"username", "password":"password"})

        self.assertEqual(int((self.client.session['_auth_user_id'])), self.user.id)

    def test_postBadTemplate(self):
        r=self.client.post("/login/", {"name":"incorrect", "password":"alsoincorrectpassword"}, follow=True)
        self.assertEqual(r.templates[0].name, "login.html")

    def test_postBadUrl(self):
        r=self.client.post("/login/", {"name":"incorrect", "password":"alsoincorrect"}, follow=True)
        self.assertEqual(r.context.request.path, "/login/")

    def test_postBadSession(self):
        r=self.client.post("/login/", {"name":"incorrect", "password":"alsoincorrect"}, follow=True)
        self.assertEqual(len(self.client.session.keys()),0)

    def test_postMissingInput(self):
        r=self.client.post("/login/", {"name":"", "password":""}, follow=True)
        self.assertEqual(r.templates[0].name, "login.html")

    def test_postDuplicateWrongInput(self):
        r=self.client.post("/login/", {"name":"incorrect", "password":"incorrect"})
        self.assertEqual(r.templates[0].name, "login.html")

    def test_postDuplicateCorrectInput(self):
        user2=User.objects.create_user("correct", "blahblah@gmail.com", "correct")
        user2.save()

        r=self.client.post("/login/", {"name":"correct", "password":"correct"}, follow=True)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user2.id)



    def test_postMissingUser(self):
        r=self.client.post("/login/", {"name":"", "password":"password"}, follow=True)
        self.assertEqual(r.templates[0].name, "login.html")

    def test_postMissingPass(self):
        r=self.client.post("/login/", {"name":"username", "password":""}, follow=True)
        self.assertEqual(r.templates[0].name, "login.html")


    def test_postMultiLoginAccount1(self):
        self.client.post("/login/", {"name": "username", "password": "password"})

        user2=User.objects.create_user("Jimbo Jones", "jimbo@gmail.com", "jimbospassword")

        user2.save()

        client2=Client()

        client2.post("/login/", {"name":"Jimbo Jones", "password":"jimbospassword"}, follow=True)

        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)


    def test_postMultiLoginAccount2(self):



        self.client.post("/login/", {"name": "username", "password": "password"})

        user2=User.objects.create_user("Jimbo Jones", "jimbo@gmail.com", "jimbospassword")

        user2.save()

        client2 = Client()

        client2.post("/login/", {"name": user2.username, "password": "jimbospassword"}, follow=True)

        self.assertEqual(int(client2.session['_auth_user_id']), user2.id)




    def test_postMultiLoginFail(self):
        self.client.post("/login/", {"name": "username", "password": "password"})

        user2 = User.objects.create_user("Jimbo Jones", "jimbo@gmail.com", "jimbospassword")

        user2.save()

        client2 = Client()

        client2.post("/login/", {"name": user2.username, "password": "jimbospassword1"}, follow=True)

        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)



