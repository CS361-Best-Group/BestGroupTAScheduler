from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from TAScheduler.views import determineRole

from TAScheduler.models import Course, Section, Profile


from TAScheduler.views import AccountManagement
#no client
#
class TestdetermineRole(TestCase):


    def setUp(self):
        self.User1=User.objects.create_user(username="Alpharius Omegon", password="XX", email="AlphaLegion@imperium.com")
        self.User1.save()
        taGroup=Group.objects.get_or_create(name="ta")
        managerGroup=Group.objects.get_or_create(name="manager")
        instructorGroup=Group.objects.get_or_create(name="instructor")



    def test_adminRole(self):
        admingroup = Group.objects.get(name="manager")
        self.User1.groups.add(admingroup)
        self.assertEqual("manager", determineRole(self.User1))

    def test_instructorRole(self):
        instructorgroup = Group.objects.get(name="instructor")
        self.User1.groups.add(instructorgroup)
        self.assertEqual("instructor", determineRole(self.User1))

    def test_taRole(self):
        tagroup = Group.objects.get(name="ta")
        self.User1.groups.add(tagroup)
        self.assertEqual("ta", determineRole(self.User1))






class TestAccountManagementLoad(TestCase):

    def setUp(self):
        User1=User.objects.create_user(username="Lionel Johnson", password="I", email="darkangels@imperium.com")

        User2=User.objects.create_user(username="Fulgrim", password="III", email="emperor'schildren@imperium.com")

        User3=User.objects.create_user(username="Perturabo", password="IV", email="ironwarriors@imperium@gmail.com")

        User1.save()
        User2.save()
        User3.save()


        Profile1=Profile(user=User1, address="Caliban", phone="414-412-5345", alt_email="loyalist@imperium.com")
        Profile1.save()

        Profile2=Profile(user=User2, address="Chemos", phone="414-432-2345", alt_email="traitor@chaos.com")
        Profile2.save()


        Profile3=Profile(user=User3, address="Olympia", phone="414-412-2409", alt_email="traitor@chaos.com")
        Profile3.save()


        self.TAUser=User.objects.create_user(username="TA", password="TA", email="ta@gmail.com")
        self.TAUser.save()


        self.InstructorUser=User.objects.create_user(username="Malcador", password="password", email="whatami@imperium.com")
        self.InstructorUser.save()
        self.AdminUser=User.objects.create_user(username="Emperor of Mankind", password="idiot", email="badfather@imperium.com")
        self.AdminUser.save()
        taGroup=Group.objects.get_or_create(name="ta")
        managerGroup=Group.objects.get_or_create(name="manager")
        instructorGroup=Group.objects.get_or_create(name="instructor")

        actualTAGroup = Group.objects.filter(name='ta')[0]
        actualInstructorGroup = Group.objects.filter(name="instructor")[0]
        actualmanagerGroup= Group.objects.filter(name="manager")[0]

        self.TAUser.groups.add(actualTAGroup)

        self.InstructorUser.groups.add(actualInstructorGroup)

        self.AdminUser.groups.add(actualmanagerGroup)

    def test_correctUserObjectsTA(self):

        self.assertEqual(list(AccountManagement.load(AccountManagement, self.TAUser)[0]), list(User.objects.all()))

    def test_returnCorrectUserObjectsInstructor(self):
        self.assertEqual(list(AccountManagement.load(AccountManagement,self.InstructorUser)[0]), list(User.objects.all()))
    def test_returnCorrectUserObjectsAdmin(self):
        self.assertEqual(list(AccountManagement.load(AccountManagement, self.AdminUser)[0]), list(User.objects.all()))

    def test_returnCorrectProfileObjectsTA(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.TAUser)[1], [])
    def test_returnCorrectProfileObjectsInstructor(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.InstructorUser)[1], [])

    def test_returnCorrectProfileObjectsAdmin(self):
        self.assertEqual(list(AccountManagement.load(AccountManagement, self.AdminUser)[1]), list(Profile.objects.all()))

    def test_returnCorrectSideButtonsTA(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.TAUser)[2], [])
    def test_returnCorrectSideButtonsInstructor(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.InstructorUser)[2], [])

    def test_returnCorrectSideButtonsAdmin(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.AdminUser)[2][0].value, "Create" )

    def test_returnCorrectUserButtonsTA(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.TAUser)[3], [])

    def test_returnCorrectUserButtonsInstructor(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.InstructorUser)[3], [])

    def test_returnCorrectUserButtonsAdmin(self):
        self.assertEqual(AccountManagement.load(AccountManagement, self.AdminUser)[3][0].value, "Delete")



    # No users's exist
    def test_noUsers(self):
        pass
    #don't pass in a user but users do exist
    def test_noUserPassedIn(self):
        pass




