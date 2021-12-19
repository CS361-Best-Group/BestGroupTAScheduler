from django.test import TestCase
from django.contrib.auth.models import User
from TAScheduler.views import AccountManagement
from django.db.utils import IntegrityError


class TestCreateUser(TestCase):
    def setUp(self):
        self.userA = {"username": "UserA",
                      "email": "user@uwm.edu",
                      "name": "NewUser",
                      "password": "password",
                      "address": "123 Some St",
                      "phone": "1234567890",
                      "altemail": "user@gmail.com",
                      "groups": "manager"}
        self.userA2 = {"username": "UserA",
                       "email": "user@uwm.edu",
                       "name": "NewUser",
                       "password": "password",
                       "address": "123 Some St",
                       "phone": "1234567890",
                       "altemail": "user@gmail.com",
                       "groups": "manager"}
        self.userI = {"username": "UserI",
                      "email": "useri@uwm.edu",
                      "name": "Instructor",
                      "password": "passstudent",
                      "address": "123 This St",
                      "phone": "1234567899",
                      "altemail": "useri@gmail.com",
                      "groups": "instructor"}
        self.userT = {"username": "UserT",
                      "email": "usert@uwm.edu",
                      "name": "TA",
                      "password": "passclass",
                      "address": "123 That St",
                      "phone": "1234567888",
                      "altemail": "usert@gmail.com",
                      "groups": "ta"}

    def test_Init_Admin(self):
        AccountManagement.createUser(AccountManagement, self.userA)
        # check that userA was added to database
        self.assertTrue(len(User.objects.filter(username="UserA")) == 1)

    def tests_Init_Instructor(self):
        AccountManagement.createUser(AccountManagement, self.userI)
        self.assertTrue(len(User.objects.filter(username="UserI")) == 1)

    def tests_Init_TA(self):
        AccountManagement.createUser(AccountManagement, self.userT)
        self.assertTrue(len(User.objects.filter(username="UserT")) == 1)


class TestDeleteUser(TestCase):
    def setUp(self):
        self.userA = {"username": "UserAdm",
                      "email": "user@uwm.edu",
                      "name": "NewUser",
                      "password": "password",
                      "address": "123 Some St",
                      "phone": "1234567890",
                      "altemail": "user@gmail.com",
                      "groups": "manager"}
        self.userI = {"username": "UserIns",
                      "email": "useri@uwm.edu",
                      "name": "Instructor",
                      "password": "passstudent",
                      "address": "123 This St",
                      "phone": "1234567899",
                      "altemail": "useri@gmail.com",
                      "groups": "instructor"}
        self.userT = {"username": "UserTA",
                      "email": "usert@uwm.edu",
                      "name": "TA",
                      "password": "passclass",
                      "address": "123 That St",
                      "phone": "1234567888",
                      "altemail": "usert@gmail.com",
                      "groups": "ta"}

    def test_delete_Admin(self):
        # Creating a user to test delete
        AccountManagement.createUser(AccountManagement, self.userA)
        # delete user
        AccountManagement.deleteUser(AccountManagement, {"username": "UserAdm"})
        # check that user was fully deleted
        self.assertTrue(len(User.objects.filter(username="UserAdm")) == 0)

    def test_delete_Instructor(self):
        AccountManagement.createUser(AccountManagement, self.userI)
        AccountManagement.deleteUser(AccountManagement, {"username": "UserIns"})
        self.assertTrue(len(User.objects.filter(username="UserIns")) == 0)

    def test_delete_TA(self):
        AccountManagement.createUser(AccountManagement, self.userT)
        AccountManagement.deleteUser(AccountManagement, {"username": "UserTA"})
        self.assertTrue(len(User.objects.filter(username="UserTA")) == 0)


class TestDetermineForm(TestCase):
    def setUp(self):
        self.create = {"username": "UserN",
                       "email": "usern@uwm.edu",
                       "name": "NewUser",
                       "password": "passdrow",
                       "address": "123 This St",
                       "phone": "1234567899",
                       "altemail": "usern@gmail.com",
                       "groups": "manager"}
        self.delete = {"username": "UserN"}
        self.other = {"name": "NewUser"}
        self.empty = {"": ""}

    def test_createForm(self):
        AccountManagement.determineForm(AccountManagement, self.create)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 1)

    def test_deleteForm(self):
        AccountManagement.determineForm(AccountManagement, self.create)
        AccountManagement.determineForm(AccountManagement, self.delete)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 0)

    def test_otherForm(self):
        AccountManagement.determineForm(AccountManagement, self.other)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 0)

    def test_emptyForm(self):
        AccountManagement.determineForm(AccountManagement, self.empty)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 0)

