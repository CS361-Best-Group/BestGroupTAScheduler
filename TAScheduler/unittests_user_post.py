import unittest
from django.contrib.auth.models import User
from TAScheduler.views import AccountManagement


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        self.userA = {"username": "User",
                      "email": "user@uwm.edu",
                      "name": "NewUser",
                      "password": "password",
                      "address": "123 Some St",
                      "phone": "1234567890",
                      "altemail": "user@gmail.com",
                      "groups": "admin"}
        self.userA2 = {"username": "User",
                       "email": "user@uwm.edu",
                       "name": "NewUser",
                       "password": "password",
                       "address": "123 Some St",
                       "phone": "1234567890",
                       "altemail": "user@gmail.com",
                       "groups": "admin"}
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
        AccountManagement.createUser(self, self.userA)
        # check that gooduser was added to database
        self.assertTrue(len(User.objects.filter(username="User")) == 1)

    def tests_Init_Instructor(self):
        AccountManagement.createUser(self, self.userI)
        self.assertTrue(len(User.objects.filter(username="UserI")) == 1)

    def tests_Init_TA(self):
        AccountManagement.crewateUser(self, self.userT)
        self.assertTrue(len(User.objects.filter(username="UserT")) == 1)

    def test_DupUser(self):
        AccountManagement.createUser(self, self.userA)
        # Throw error as userA2 uses the same username as userA
        # Do not add userA2
        with self.assertRaises(ValueError, msg="Duplicate Username"):
            AccountManagement.createUser(self, self.userA2)


class TestDeleteUser(unittest.TestCase):
    def setUp(self):
        self.userA = {"username": "UserAdm",
                      "email": "user@uwm.edu",
                      "name": "NewUser",
                      "password": "password",
                      "address": "123 Some St",
                      "phone": "1234567890",
                      "altemail": "user@gmail.com",
                      "groups": "admin"}
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
        AccountManagement.createUser(self, self.userA)
        # delete user
        AccountManagement.deleteUser(self, self.userA["username"])
        # check that user was fully deleted
        self.assertTrue(len(User.objects.filter(username="UserAdm")) == 0)

    def test_delete_Instructor(self):
        AccountManagement.createUser(self, self.userI)
        AccountManagement.deleteUser(self, self.userI["username"])
        self.assertTrue(len(User.objects.filter(username="UserIns")) == 0)

    def test_delete_TA(self):
        AccountManagement.createUser(self, self.userT)
        AccountManagement.deleteUser(self, self.userT["username"])
        self.assertTrue(len(User.objects.filter(username="UserTA")) == 0)

    def test_delete_NoUser(self):
        with self.assertRaises(KeyError, msg="No user to delete"):
            AccountManagement.deleteUser(self, self.userA["username"])


class TestDetermineForm(unittest.TestCase):
    def setUp(self):
        self.create = {"username": "UserN",
                       "email": "usern@uwm.edu",
                       "name": "NewUser",
                       "password": "passdrow",
                       "address": "123 This St",
                       "phone": "1234567899",
                       "altemail": "usern@gmail.com",
                       "group__name": "admin"}
        self.delete = {"username": "UserN"}
        self.other = {"name": "NewUser"}
        self.empty = {""}

    def test_createForm(self):
        AccountManagement.determineForm(self, self.create)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 1)

    def test_deleteForm(self):
        AccountManagement.determineForm(self, self.create)
        AccountManagement.determineForm(self, self.delete)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 0)

    def test_otherForm(self):
        with self.assertRaises(ValueError, msg="Didn't receive 'deleteUser' xor 'createUser'"):
            AccountManagement.determineForm(self, self.other)

    def test_emptyForm(self):
        with self.assertRaises(ValueError, msg="Can't have empty key for input"):
            AccountManagement.determineForm(self, self.empty)