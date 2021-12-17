from django.test import TestCase
from django.contrib.auth.models import User
from TAScheduler.views import AccountManagement


class TestCreateUser(TestCase):
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
        AccountManagement.createUser(AccountManagement, self.userA)
        # check that userA was added to database
        self.assertTrue(len(User.objects.filter(username="User")) == 1)

    def tests_Init_Instructor(self):
        AccountManagement.createUser(AccountManagement, self.userI)
        self.assertTrue(len(User.objects.filter(username="UserI")) == 1)

    def tests_Init_TA(self):
        AccountManagement.createUser(AccountManagement, self.userT)
        self.assertTrue(len(User.objects.filter(username="UserT")) == 1)

    # throws error if trying to create a duplicate username --> user
    def test_DupUser(self):
        AccountManagement.createUser(AccountManagement, self.userA)
        # Throw error as userA2 uses the same username as userA
        # Do not add userA2
        with self.assertRaises(ValueError, msg="Duplicate Username"):
            AccountManagement.createUser(AccountManagement, self.userA2)


class TestDeleteUser(TestCase):
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
        AccountManagement.createUser(AccountManagement, self.userA)
        # delete user
        AccountManagement.deleteUser(AccountManagement, self.userA["username"])
        # check that user was fully deleted
        self.assertTrue(len(User.objects.filter(username="UserAdm")) == 0)

    def test_delete_Instructor(self):
        AccountManagement.createUser(AccountManagement, self.userI)
        AccountManagement.deleteUser(AccountManagement, self.userI["username"])
        self.assertTrue(len(User.objects.filter(username="UserIns")) == 0)

    def test_delete_TA(self):
        AccountManagement.createUser(AccountManagement, self.userT)
        AccountManagement.deleteUser(AccountManagement, self.userT["username"])
        self.assertTrue(len(User.objects.filter(username="UserTA")) == 0)

    # throws error if trying to delete a user that does not exist
    def test_delete_NoUser(self):
        with self.assertRaises(KeyError, msg="No user to delete"):
            AccountManagement.deleteUser(AccountManagement, self.userA["username"])


class TestDetermineForm(TestCase):
    def setUp(self):
        self.create = {"username": "UserN",
                       "email": "usern@uwm.edu",
                       "name": "NewUser",
                       "password": "passdrow",
                       "address": "123 This St",
                       "phone": "1234567899",
                       "altemail": "usern@gmail.com",
                       "groups": "admin"}
        self.delete = {"username": "UserN"}
        self.other = {"name": "NewUser"}
        self.empty = {""}

    def test_createForm(self):
        AccountManagement.determineForm(AccountManagement, self.create)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 1)

    def test_deleteForm(self):
        AccountManagement.determineForm(AccountManagement, self.create)
        AccountManagement.determineForm(AccountManagement, self.delete)
        self.assertTrue(len(User.objects.filter(username="UserN")) == 0)

    # throws error if it gets passed a form other than whats expected (create or delete)
    def test_otherForm(self):
        with self.assertRaises(ValueError, msg="Didn't receive 'deleteUser' xor 'createUser'"):
            AccountManagement.determineForm(AccountManagement, self.other)

