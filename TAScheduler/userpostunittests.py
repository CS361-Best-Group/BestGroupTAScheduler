import unittest

from django.contrib.auth.models import User

from TAScheduler.views import AccountManagement


#    post method()
#         determiningmethod()
#             form1method
#             or form2 method
#             or form3method
#             or etc
#    return redirect(currentpage)

class TestUserPostMethods(unittest.TestCase):

    def test_post(self):
        pass

    def test_DetermineForm(self, request):
        # Calls the appropriate form method.
        # Determines which form method to call based on the presence/absence of certain keys in the post dictionary.
        # if form==deleteUser then deleteUserForm
        # else if form==createUser then createUserForm
        # else error
        self.assertTrue(("deleteUser" in request.POST.keys() and not "createUser" in request.POST.keys())
                        or ("createUser" in request.POST.keys() and not "deleteUser" in request.POST.keys()))
        with self.assertRaises(ValueError, msg="Didn't receive 'deleteUser' or 'createUser'"):
            AccountManagement.determineForm(self, "anotherMethod")

    def test_deleteUser(self, request):
        # what am i testing for?
        # - correct user is deleted
        user = AccountManagement.createUser(username="NewUser", email="nu@uwm.edu", name="User",
                                            password="password", address="123 Some St", phone="1234567890",
                                            altemail="nu@gmail.com", groups__name="ta")
        AccountManagement.deleteUser(username="NewUser")
        self.assertTrue(len(User.objects.filter(username=user.username)) == 0)

    def test_createUser(self, request):
        # what do I need to test for?
        # create a valid user: non repeating username, assumes all info given
        # username, email, name, password, address, phone, altemail, group?

        gooduser = AccountManagement.createUser(username="NewUser", email="nu@uwm.edu", name="User",
                                                password="password", address="123 Some St", phone="1234567890",
                                                altemail="nu@gmail.com", groups__name="ta")
        # check that gooduser was added to database
        self.assertTrue(len(User.objects.filter(username=gooduser.username)) == 1)
        # confirm that the current user is good
        self.assertTrue(gooduser.username == "NewUser" and gooduser.email == "nu@uwm.edu" and gooduser.name == "User"
                        and gooduser.password == "password" and gooduser.address == "123 Some St" and
                        gooduser.phone == "1234567890" and gooduser.altemail == "nu@gmail.com" and
                        gooduser.groups__name == "ta")
        # Throw error as baduser1 uses the same username as gooduser
        with self.assertRaises(ValueError, msg="Duplicate Username"):
            baduser = AccountManagement.createUser(username="NewUser", email="nu@uwm.edu", name="User",
                                                   password="password", address="123 Some St", phone="1234567890",
                                                   altemail="nu@gmail.com", groups__name="ta")
        # confirm that only good user is in the database
        self.assertTrue(len(User.objects.filter(name=gooduser.name)) == 1)
