from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class TestAccountCreationGet(TestCase):

    def setUp(self):
        self.client=Client()
        #need to make this the model and adjust tests accordingly, then mess with code.
        TA=User.objects.create_user("Timmy", "timmy@gmail.com", "password", first_name="TA Timmy")
        self.ta_group, created= Group.objects.get_or_create(name='ta')
        TA.groups.add(self.ta_group)

        Instructor=User.objects.create_user("Isaac", "issac@gmail.com", "betterpassword", first_name="Instructor Isaac")
        self.instructor_group, created=Group.objects.get_or_create(name='instructor')

        Instructor.groups.add(self.instructor_group)

        Admin=User.objects.create_user("Adam", "adam@gmail.com", "bestpassW1rd", first_name="Admin Adam")
        self.admin_group, created=Group.objects.get_or_create(name="manager")
        Admin.groups.add(self.admin_group)

        TA.save()
        Instructor.save()
        Admin.save()



    def test_loadTAName(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].first_name, "TA Timmy")

    def test_displayTAName(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">TA Timmy</div>' )


    def test_loadTAPrimaryEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].email, "timmy@gmail.com")

    def test_displayTAPrimaryEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">timmy@gmail.com</div>')

    def test_loadTAAlternateEmail(self):
        pass
    def test_displayTAAlternameEmail(self):
        pass

    def test_loadInstructorName(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].first_name, "Instructor Isaac")

    def test_displayInstructorName(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">Instructor Isaac</div>')

    def test_loadInstructorEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].email, "issac@gmail.com")

    def test_displayInstructorEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">issac@gmail.com</div>')

    def test_loadInstructorAltEmail(self):
        pass


    def test_loadAdminName(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].first_name, "Admin Adam")

    def test_displayAdminName(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">Admin Adam</div>')

    def test_loadAdminEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].email, "adam@gmail.com")
    def test_displayAdminEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">adam@gmail.com</div>')
    def test_loadMultuipleTAName(self):
        TA2=User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][1].first_name, "TA Tyler")

    def test_displayMultipleTAName1(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">TA Timmy</div>')
    def test_displayMultipleTAName2(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">TA Tyler</div>')
    def test_loadMultipleTAEmail(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][1].email, "tyler@gmail.com")

    def test_displayMultipleTAEmail1(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">timmy@gmail.com</div>')
    def test_displayMultipleTAEmail2(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">tyler@gmail.com</div>')

    def test_loadMultipleInstructorName(self):
        IN2=User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][1].first_name, "Instructor Ivy")

    def test_displayMultyipleInstructorName1(self):
        IN2 = User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">Instructor Isaac</div>')
    def test_displayMultipleInstructorName2(self):
        IN2 = User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">Instructor Ivy</div>')

    def test_loadMultipleInstructorEmail(self):
        IN2=User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][1].email, "ivy@gmail.com")

    def test_displayMultipleInstructorEmail1(self):
        IN2 = User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">issac@gmail.com</div>')
    def test_displayMultipleInstructorEmail2(self):
        IN2 = User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">ivy@gmail.com</div>')


    def test_loadMultipleAdminName(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][1].first_name, "Admin Avery")

    def test_displayMultipleAdminName1(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">Admin Adam</div>')
    def test_displayMultipleAdminName2(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="name">Admin Avery</div>')


    def test_loadMultipleAdminEmail(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][1].email, "avery@gmail.com")

    def test_displayMultipleAdminEmail1(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">adam@gmail.com</div>')
    def test_displayMultipleAdminEmail2(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, '<div class="email">avery@gmail.com</div>')




class TestAccountCreationPost(TestCase):

    def setUp(self):
        self.client=Client()
        self.admin_group, created = Group.objects.get_or_create(name="manager")

        self.r=self.client.post("/accountmanagement/", {"username":"Testing123", "password":"sword1", "email":"testing@gmail.com", "name":"Manager Marcus"}, follow=True)

    def test_newAccount(self):
        self.assertEqual(len(User.objects.all()), 1)

    def test_displayNewAccountName(self):
        self.assertContains(self.r ,'<div class="name">Manager Marcus</div>')

    def test_displayNewAccountEmail(self):
        self.assertContains(self.r, '<div class="email">testing@gmail.com</div>')

    def test_usernameStored(self):
        self.assertEqual(User.objects.all()[0].username, "Testing123")

    def test_emailStored(self):
        self.assertEqual(User.objects.all()[0].email,"testing@gmail.com")

    def test_passwordStored(self):
        self.assertNotEqual(User.objects.all()[0].password, None)

    def test_nameStored(self):
        self.assertEqual(User.objects.all()[0].first_name, "Manager Marcus")


    def test_userGroup(self):
        self.assertEqual(User.objects.all()[0].groups.all()[0].name,'manager')

    def test_secondNewAccount(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(len(User.objects.all()), 2)
    def test_secondNewAccountUser(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(User.objects.all()[1].username, "Testing1234")


    def test_secondNewAccountEmail(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(User.objects.all()[1].email, "testing4@gmail.com")

    def test_secondNewAccountName(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(User.objects.all()[1].first_name, "Manager Maria")

    def test_secondAccountPassword(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertNotEqual(User.objects.all()[1].password, None)


    def test_secondNewAccountGroup(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)

        self.assertEqual(User.objects.all()[1].groups.all()[0].name, 'manager')




    def test_displaySecondNewAccountName(self):
        r=self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertContains(r, '<div class="name">Manager Maria</div>')

    def test_displaySecondNewAccountEmail(self):
        r=self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertContains(r, '<div class="email">testing4@gmail.com</div>')


    def test_duplicateUser(self):
        self.client.post("/accountmanagement/", {"username":"Testing123", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(len(User.objects.all()), 1)

    def test_duplicateUserKeepEmail(self):
        self.client.post("/accountmanagement/", {"username":"Testing123", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(User.objects.all()[0].email, "testing@gmail.com")

    def test_duplicatePassword(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"sword1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(len(User.objects.all()), 2)

    #entering same username and password when creating a geniuenly new account
    def test_duplicateUserandPassword(self):
        self.client.post("/accountmanagement/", {"username":"shield1", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria"}, follow=True)
        self.assertEqual(len(User.objects.all()),2)

    def test_passwordHashed(self):
        self.assertNotEqual(User.objects.all()[0].password, "sword1")

    #Need to figure out exactly what duplicates are allowed, other than that, this has my thumbs up!