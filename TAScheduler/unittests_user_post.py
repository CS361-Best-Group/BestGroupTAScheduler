import unittest
from django.contrib.auth.models import User
from TAScheduler.views import AccountManagement


class TestUserPostMethods(unittest.TestCase):

    def test_createUser(self):
        # create a valid user: non repeating username, assumes all info given
        # username, email, name, password, address, phone, altemail, group(ta,instructor,manager)

        gooduser = AccountManagement.createUser(username="NewUser", email="nu@uwm.edu", name="User",
                                                password="password", address="123 Some St", phone="1234567890",
                                                altemail="nu@gmail.com", groups__name="ta")
        # check that gooduser was added to database
        self.assertTrue(len(User.objects.filter(username=gooduser.username)) == 1)
        # confirm that the current user is good
        self.assertTrue(gooduser.username == "NewUser")
        self.assertTrue(gooduser.email == "nu@uwm.edu")
        self.assertTrue(gooduser.name == "User")
        self.assertTrue(gooduser.password == "password")
        self.assertTrue(gooduser.address == "123 Some St")
        self.assertTrue(gooduser.phone == "1234567890")
        self.assertTrue(gooduser.altemail == "nu@gmail.com")
        self.assertTrue(gooduser.groups__name == "ta")
        # Throw error as baduser uses the same username as gooduser, and does not add baduser
        with self.assertRaises(ValueError, msg="Duplicate Username"):
            baduser = AccountManagement.createUser(username="NewUser", email="nu@uwm.edu", name="User",
                                                   password="password", address="123 Some St", phone="1234567890",
                                                   altemail="nu@gmail.com", groups__name="ta")
        # confirm that only gooduser is in the database
        # this also confirms if gooduser is still in the database
        self.assertTrue(len(User.objects.filter(username=gooduser.username)) == 1)

    def test_deleteUser(self):
        # correct user is deleted
        AccountManagement.createUser(username="NewUser", email="nu@uwm.edu", name="User",
                                     password="password", address="123 Some St", phone="1234567890",
                                     altemail="nu@gmail.com", groups__name="ta")
        AccountManagement.deleteUser(username="NewUser")
        self.assertTrue(len(User.objects.filter(username="NewUser")) == 0)
        self.assertTrue(len(User.objects.filter(email="nu@uwm.edu")) == 0)
        self.assertTrue(len(User.objects.filter(name="User")) == 0)
        self.assertTrue(len(User.objects.filter(password="password")) == 0)
        self.assertTrue(len(User.objects.filter(address="123 Some St")) == 0)
        self.assertTrue(len(User.objects.filter(phone="1234567890")) == 0)
        self.assertTrue(len(User.objects.filter(altemail="nu@gmail.com")) == 0)
        self.assertTrue(len(User.objects.filter(group__name="ta")) == 0)

    def test_determineForm(self, request):
        # Calls the appropriate form method.
        # Determines which form method to call based on the presence/absence of certain keys in the post dictionary.
        # if form==deleteUser then deleteUserForm
        # else if form==createUser then createUserForm
        # else error
        # Need dummy dictionary to pass into determineForm

        dictcreate = {"input": "createUser",
                      "username": "UserN",
                      "email": "usern@uwm.edu",
                      "name": "NewUser",
                      "password": "passdrow",
                      "address": "123 This St",
                      "phone": "1234567899",
                      "altemail": "usern@gmail.com",
                      "group__name": "admin"}
        dictdelete = {"input": "createUser",
                      "username": "UserN",
                      "email": "usern@uwm.edu",
                      "name": "NewUser",
                      "password": "passdrow",
                      "address": "123 This St",
                      "phone": "1234567899",
                      "altemail": "usern@gmail.com",
                      "group__name": "admin"}
        dictanother = {"input": "anotherMethod"}
        dictempty = {"input": ""}

        AccountManagement.determineForm(self, dictcreate)

        self.assertTrue(len(User.objects.filter(username="UserN")) == 1)
        self.assertTrue(len(User.objects.filter(email="usern@uwm.edu")) == 1)
        self.assertTrue(len(User.objects.filter(name="UserN")) == 1)
        self.assertTrue(len(User.objects.filter(password="passdrow")) == 1)
        self.assertTrue(len(User.objects.filter(address="123 This St")) == 1)
        self.assertTrue(len(User.objects.filter(phone="1234567899")) == 1)
        self.assertTrue(len(User.objects.filter(altemail="usern@gmail.com")) == 1)
        self.assertTrue(len(User.objects.filter(group__name="admin")) == 1)

        AccountManagement.determineForm(self, dictdelete)

        self.assertTrue(len(User.objects.filter(username="UserN")) == 0)
        self.assertTrue(len(User.objects.filter(email="usern@uwm.edu")) == 0)
        self.assertTrue(len(User.objects.filter(name="UserN")) == 0)
        self.assertTrue(len(User.objects.filter(password="passdrow")) == 0)
        self.assertTrue(len(User.objects.filter(address="123 This St")) == 0)
        self.assertTrue(len(User.objects.filter(phone="1234567899")) == 0)
        self.assertTrue(len(User.objects.filter(altemail="usern@gmail.com")) == 0)
        self.assertTrue(len(User.objects.filter(group__name="admin")) == 0)

        with self.assertRaises(ValueError, msg="Didn't receive 'deleteUser' xor 'createUser'"):
            AccountManagement.determineForm(self, dictanother)
        with self.assertRaises(ValueError, msg="Can't have empty key for input"):
            AccountManagement.determineForm(self, dictempty)
