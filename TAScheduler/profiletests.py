from django.contrib.auth import login
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Profile

class TestProfileGet(TestCase):

    def setUp(self):
        self.client=Client()

        User1=User.objects.create_user(username="TA Timmy", password="testpassword", email="timmy@gmail.com", first_name="Timmy")
        User1.save()
        Profile1=Profile(user=User1, address="9999", alt_email="nottimmy@gmail.com", phone="999-999-9999")
        Profile1.save()

        self.client.force_login(User1)


    def test_loadFirstName(self):

        r=self.client.get("/profile/")
        self.assertEqual(r.context["firstname"], "Timmy")

    def test_displayFirstName(self):
        r=self.client.get("/profile/")
        self.assertContains(r, 'Timmy')

    def test_loadEmail(self):
        r=self.client.get("/profile/")
        self.assertEqual(r.context["email"], "timmy@gmail.com")

    def test_displayEmaiL(self):
        r=self.client.get("/profile/")
        self.assertContains(r, 'timmy@gmail.com')

    def test_loadUsername(self):
        r=self.client.get("/profile/")
        self.assertEqual(r.context["username"], "TA Timmy")

    def test_displayUserName(self):
        r=self.client.get("/profile/")
        self.assertContains(r, 'TA Timmy')

    def test_loadAddress(self):
        r=self.client.get("/profile/")
        self.assertEqual(r.context["address"], "9999")

    def test_displayAddress(self):
        r=self.client.get("/profile/")
        self.assertContains(r, '9999')

    def test_loadPhone(self):
        r=self.client.get("/profile/")
        self.assertEqual(r.context["phone"], "999-999-9999")

    def test_displayPhone(self):
        r=self.client.get("/profile/")
        self.assertContains(r, '999-999-9999')

    def test_loadAltEmail(self):
        r=self.client.get("/profile/")
        self.assertEqual(r.context["altemail"], "nottimmy@gmail.com")

    def test_displayAltEmail(self):
        r=self.client.get("/profile/")
        self.assertContains(r, 'nottimmy@gmail.com')



class TestProfilePost(TestCase):

    def setUp(self):
        self.client = Client()

        self.User1 = User.objects.create_user(username="TA Timmy", password="testpassword", email="timmy@gmail.com",
                                         first_name="Timmy")
        self.User1.save()
        self.Profile1 = Profile(user=self.User1, address="9999", alt_email="nottimmy@gmail.com", phone="999-999-9999")
        self.Profile1.save()

        self.client.force_login(self.User1)

    def test_noChangeName(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].first_name, "Timmy")

    def test_noChangeUsername(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].username, "TA Timmy")

    def test_noChangeAddress(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].address, "9999")

    def test_noChangePhone(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].phone, "999-999-9999")

    def test_noChangeEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].email, "timmy@gmail.com")

    def test_noChangeAltEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].alt_email, "nottimmy@gmail.com")
    #ignore changes to username

    def test_duplicateUsername(self):
        User2 = User.objects.create_user(username="TA Tyler", password="differentpassword", email="tyler@gmail.com", first_name="Tyler")
        User2.save()
        Profile2=Profile(user=User2, address="9998", alt_email="alt@gmail.com", phone="999-999-9998")
        Profile2.save()
        self.client.post("/profile/", {"username":User2.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].username, "TA Timmy")



    def test_changeEverythingName(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(User.objects.all()[0].first_name, "New Name")

    def test_changeEverythingUsername(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(User.objects.all()[0].username, "New Username")

    def test_changeEverythingAddress(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(Profile.objects.all()[0].address, "New Address")

    def test_changeEverythingPhone(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(Profile.objects.all()[0].phone, "111-111-1111")

    def test_changeEverythingEmail(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(User.objects.all()[0].email, "newemail@gmail.com")

    def test_changeEverythingAltEmail(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(Profile.objects.all()[0].alt_email, "newaltemail@gmail.com")


    def test_changeName(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":"New Name", "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].first_name, "New Name")

    def test_changeUsername(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].username, "New Username")

    def test_changeAddress(self):

        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":"1111", "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].address, "1111")

    def test_changePhone(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":"111-111-1111", "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].phone, "111-111-1111")

    def test_changeEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":"newemail@gmail.com", "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].email, "newemail@gmail.com")

    def test_changeAltEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertEqual(Profile.objects.all()[0].alt_email, "newaltemail@gmail.com")

    #can't have empty, it just stays how it is
    def test_emptyName(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":"", "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].first_name, "Timmy")

    def test_emptyUsername(self):
        r=self.client.post("/profile/", {"username":"", "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].username, "TA Timmy")

    def test_emptyAddress(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":"", "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].address, "9999")

    def test_emptyPhone(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":"", "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(Profile.objects.all()[0].phone, "999-999-9999")

    def test_emptyEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":"", "altemail":self.Profile1.alt_email}, follow=True)
        self.assertEqual(User.objects.all()[0].email, "timmy@gmail.com")

    def test_emptyAltEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":""}, follow=True)
        self.assertEqual(Profile.objects.all()[0].alt_email, "nottimmy@gmail.com")

    def test_displayNewName(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":"New Name", "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'New Name')

    def test_displayNewUsername(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'New Username')

    def test_displayNewAddress(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":"1111", "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, '1111')

    def test_displayNewPhone(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":"111-111-1111", "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, '111-111-1111')

    def test_displayNewEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":"newemail@gmail.com", "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'newemail@gmail.com')

    def test_displayNewAltEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, 'newaltemail@gmail.com')

    def test_displayChangeEverythingName(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, 'New Name')

    def test_displayChangeEverythingUsername(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, 'New Username')

    def test_displayChangeEverythingAddress(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, 'New Address')

    def test_displayChangeEverythingPhone(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, '111-111-1111')

    def test_displayChangeEverythingEmail(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, 'newemail@gmail.com')

    def test_displayChangeEverythingAltEmail(self):
        r=self.client.post("/profile/", {"username":"New Username", "name":"New Name", "address":"New Address", "phone":"111-111-1111", "email":"newemail@gmail.com", "altemail":"newaltemail@gmail.com"}, follow=True)
        self.assertContains(r, 'newaltemail@gmail.com')

    def test_displayChangeNothingName(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'Timmy')

    def test_displayChangeNothingUsername(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'TA Timmy')

    def test_displayChangeNothingAddress(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, '9999')

    def test_displayChangeNothingPhone(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, '999-999-9999')

    def test_displayChangeNothingEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'timmy@gmail.com')

    def test_displayChangeNothingAltEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'nottimmy@gmail.com')

    def test_displayEmptyName(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":"", "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'Timmy')

    def test_displayEmptyUsername(self):
        r=self.client.post("/profile/", {"username":"", "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'TA Timmy')

    def test_displayEmptyAddress(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":"", "phone":self.Profile1.phone, "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, '9999')

    def test_displayEmptyPhone(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":"", "email":self.User1.email, "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, '999-999-9999')


    def test_displayEmptyEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":"", "altemail":self.Profile1.alt_email}, follow=True)
        self.assertContains(r, 'nottimmy@gmail.com')

    def test_displayEmptyAltEmail(self):
        r=self.client.post("/profile/", {"username":self.User1.username, "name":self.User1.first_name, "address":self.Profile1.address, "phone":self.Profile1.phone, "email":self.User1.email, "altemail":""}, follow=True)
        self.assertContains(r, 'nottimmy@gmail.com')
