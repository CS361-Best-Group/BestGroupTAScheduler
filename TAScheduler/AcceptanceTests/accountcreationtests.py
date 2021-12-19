from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from TAScheduler.models import Profile

class TestAccountCreationGet(TestCase):

    def setUp(self):
        self.client=Client()
        #need to make this the model and adjust tests accordingly, then mess with code.
        self.TA=User.objects.create_user("Timmy", "timmy@gmail.com", "password", first_name="TA Timmy")
        self.ta_group, created= Group.objects.get_or_create(name='ta')
        self.TA.groups.add(self.ta_group)



        self.Instructor=User.objects.create_user("Isaac", "issac@gmail.com", "betterpassword", first_name="Instructor Isaac")
        self.instructor_group, created=Group.objects.get_or_create(name='instructor')

        self.Instructor.groups.add(self.instructor_group)

        Admin=User.objects.create_user("Adam", "adam@gmail.com", "bestpassW1rd", first_name="Admin Adam")
        self.admin_group, created=Group.objects.get_or_create(name="manager")
        Admin.groups.add(self.admin_group)

        self.TA.save()
        self.Instructor.save()
        Admin.save()

        TAProfile=Profile(user=self.TA, address="9999", phone="999-999-9999", alt_email="alt@gmail.com")
        TAProfile.save()

        InstructorProfile=Profile(user=self.Instructor, address="9998", phone="999-999-9998", alt_email="alt2@gmail.com")
        InstructorProfile.save()


        AdminProfile=Profile(user=Admin, address="9997", phone="999-999-9997", alt_email="alt3@gmail.com")
        AdminProfile.save()

        self.client.force_login((Admin))
    def test_loadTAName(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].first_name, "TA Timmy")

    def test_displayTAName(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'TA Timmy' )


    def test_loadTAPrimaryEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].email, "timmy@gmail.com")

    def test_displayTAPrimaryEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'timmy@gmail.com')

    def test_loadTAAlternateEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="TA Timmy")[0])[0].alt_email, "alt@gmail.com")
    def test_displayTAAlternameEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'alt@gmail.com')

    def test_loadTAAddress(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="TA Timmy")[0])[0].address, "9999")
    def test_displayTAAddress(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, '9999')
    def test_loadTAPhoneNumber(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="TA Timmy")[0])[0].phone, "999-999-9999")
    def test_displayTAPhoneNumber(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "999-999-9999")

    def test_loadInstructorName(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].first_name, "Instructor Isaac")

    def test_displayInstructorName(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'Instructor Isaac')

    def test_loadInstructorEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].email, "issac@gmail.com")

    def test_displayInstructorEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'issac@gmail.com')

    def test_loadInstructorAltEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="Instructor Isaac")[0])[0].alt_email, "alt2@gmail.com")
    def test_displayInstructorAltEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'alt2@gmail.com')
    def test_loadInstructorAddress(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="Instructor Isaac")[0])[0].address, "9998")
    def test_displayInstructorAddress(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "9998")
    def test_loadInstructorPhoneNumber(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="Instructor Isaac")[0])[0].phone, "999-999-9998")
    def test_displayInstructorPhoneNumber(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "999-999-9998")
    def test_loadAdminName(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].first_name, "Admin Adam")

    def test_displayAdminName(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'Admin Adam')

    def test_loadAdminEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].email, "adam@gmail.com")
    def test_displayAdminEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'adam@gmail.com')

    def test_loadAdminAltEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="Admin Adam")[0])[0].alt_email, "alt3@gmail.com")


    def test_displayAdminAltEmail(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, 'alt3@gmail.com')
    def test_loadAdminAddress(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="Admin Adam")[0])[0].address, "9997")
    def test_displayAdminAddress(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "9997")
    def test_loadAdminPhone(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"].filter(user=User.objects.filter(first_name="Admin Adam")[0])[0].phone, "999-999-9997")
    def test_displayAdminPhone(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "999-999-9997")


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
        self.assertContains(r, 'TA Timmy')
    def test_displayMultipleTAName2(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, 'TA Tyler')
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
        self.assertContains(r, 'timmy@gmail.com')
    def test_displayMultipleTAEmail2(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "The Black Knight always triumphs!", first_name="TA Tyler")
        TA2.groups.add(self.ta_group)
        TA2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, 'tyler@gmail.com')

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
        self.assertContains(r, 'Instructor Isaac')
    def test_displayMultipleInstructorName2(self):
        IN2 = User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, 'Instructor Ivy')

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
        self.assertContains(r, 'issac@gmail.com')
    def test_displayMultipleInstructorEmail2(self):
        IN2 = User.objects.create_user("Ivy", "ivy@gmail.com", "pAssword", first_name="Instructor Ivy")
        IN2.groups.add(self.instructor_group)
        IN2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, 'ivy@gmail.com')


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
        self.assertContains(r, 'Admin Adam')
    def test_displayMultipleAdminName2(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, 'Admin Avery')


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
        self.assertContains(r, 'adam@gmail.com')
    def test_displayMultipleAdminEmail2(self):
        AD2 = User.objects.create_user("Avery", "avery@gmail.com", "bestcharacter", first_name="Admin Avery")
        AD2.groups.add(self.admin_group)
        AD2.save()
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, 'avery@gmail.com')

    #######################################################################
    #NOTE: All tests above this point have a logged in admin object and can be considered admin stuff

    def test_instructorLoadTAEmail(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].email, "timmy@gmail.com")


    def test_instructorLoadInstructorEmail(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].email, "issac@gmail.com")
    def test_instructorLoadAdminEmail(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].email, "adam@gmail.com")

    def test_instructorLoadSecondUserEmail(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()
        TA2.groups.add(self.ta_group)

        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")

        self.assertEqual(r.context["TA"][1].email, "tyler@gmail.com")

    def test_instructorDisplayTAEmail(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "timmy@gmail.com")
    def test_instructorDisplayInstructorEmail(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "issac@gmail.com")

    def test_instructorDisplayAdminEmail(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "adam@gmail.com")

    def test_instructorDisplaySecondEmail(self):
        TA2=User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2=Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.client.force_login(self.Instructor)

        r = self.client.get("/accountmanagement/")

        self.assertContains(r, "tyler@gmail.com")



    def test_instructorLoadTAName(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].first_name, "TA Timmy")
    def test_instructorLoadInstructorName(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].first_name, "Instructor Isaac")

    def test_instructorLoadAdminName(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].first_name, "Admin Adam")

    def test_instructorLoadSecondUserName(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()
        TA2.groups.add(self.ta_group)


        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")

        self.assertEqual(r.context["TA"][1].first_name, "Tyler")

    def test_instructorDisplayTAName(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "TA Timmy")
    def test_instructorDisplayInstructorName(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "Instructor Isaac")
    def test_instructorDisplayAdminName(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "Admin Adam")
    def test_instructorDisplaySecondUserName(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        TA2.groups.add(self.ta_group)
        Profile2.save()

        self.client.force_login(self.Instructor)

        r = self.client.get("/accountmanagement/")

        self.assertContains(r, "Tyler")


    #end instructor stuff

    def test_taLoadTAEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].email, "timmy@gmail.com")

    def test_taLoadInstructorEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].email, "issac@gmail.com")

    def test_taLoadAdminEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].email, "adam@gmail.com")

    def test_taLoadSecondUserEmail(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()
        TA2.groups.add(self.ta_group)

        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")

        self.assertEqual(r.context["TA"][1].email, "tyler@gmail.com")

    def test_taDisplayTAEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "timmy@gmail.com")

    def test_taDisplayInstructorEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "issac@gmail.com")

    def test_taDisplayAdminEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "adam@gmail.com")

    def test_taDisplaySecondEmail(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.client.force_login(self.TA)

        r = self.client.get("/accountmanagement/")

        self.assertContains(r, "tyler@gmail.com")

    def test_taLoadTAName(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["TA"][0].first_name, "TA Timmy")

    def test_taLoadInstructorName(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Instructor"][0].first_name, "Instructor Isaac")

    def test_taLoadAdminName(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Admin"][0].first_name, "Admin Adam")

    def test_taLoadSecondUserName(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()
        TA2.groups.add(self.ta_group)

        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")

        self.assertEqual(r.context["TA"][1].first_name, "Tyler")

    def test_taDisplayTAName(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "TA Timmy")

    def test_taDisplayInstructorName(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "Instructor Isaac")

    def test_taDisplayAdminName(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        self.assertContains(r, "Admin Adam")

    def test_taDisplaySecondUserName(self):
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()
        TA2.groups.add(self.ta_group)

        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")

        self.assertContains(r, "Tyler")

    def test_taLoadProfiles(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"], [])
    def test_taLoadMultipleProfiles(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertEqual(r.context["Profiles"], [])

    def test_taDisplayTAAddress(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "9999")

    def test_taDisplayInstructorAddress(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "9998")
    def test_taDisplayAdminAddress(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "9997")




    def test_taDisplayMultipleProfilesAddress(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertNotContains(r, "9988")

    def test_taDisplayTAAltEmail(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "alt@gmail.com")
    def test_taDisplayInstructorAltEmail(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "alt2@gmail.com")

    def test_taDisplayAdminAltEmail(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "alt3@gmail.com")


    def test_taDisplayMultipleProfilesAltEmail(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertNotContains(r, "tyler2@gmail.com")

    def test_taDisplayTAPhone(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "999-999-9999")
    def test_taDisplayInstructorPhone(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "999-999-9998")
    def test_taDisplayAdminPhone(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "999-999-9997")

    def test_taDisplayMultipleProfilePhone(self):
        self.client.force_login(self.TA)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertNotContains(r, "414-124-4124")
    ###END TA TESTS

    def test_instructorLoadProfiles(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertEqual(r.context["Profiles"], [])

    def test_instructorLoadMultipleProfiles(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertEqual(r.context["Profiles"], [])

    def test_instructorDisplayTAAddress(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "9999")

    def test_instructorDisplayInstructorAddress(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "9998")

    def test_instructorDisplayAdminAddress(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "9997")
    def test_instructorDisplayMultipleProfilesAddress(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertNotContains(r, "9988")

    def test_instructorDisplayTAAltEmail(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "alt@gmail.com")

    def test_instructorDisplayInstructorAltEmail(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "alt2@gmail.com")

    def test_instructorDisplayAdminAltEmail(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "alt3@gmail.com")

    def test_instructorDisplayMultipleProfilesAltEmail(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertNotContains(r, "tyler2@gmail.com")

    def test_instructorDisplayTAPhone(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "999-999-9999")

    def test_instructorDisplayInstructorPhone(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "999-999-9998")

    def test_instructorDisplayAdminPhone(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        self.assertNotContains(r, "999-999-9997")

    def test_instructorDisplayMultipleProfilePhone(self):
        self.client.force_login(self.Instructor)
        r = self.client.get("/accountmanagement/")
        TA2 = User.objects.create_user("Tyler", "tyler@gmail.com", "Password", first_name="Tyler")
        TA2.groups.add(self.ta_group)
        Profile2 = Profile(user=TA2, address="9988", phone="414-124-4124", alt_email="tyler2@gmail.com")
        TA2.save()
        Profile2.save()

        self.assertNotContains(r, "414-124-4124")

    def test_instructorLoadSideButtons(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["SideButtons"], [])
    def test_instructorDisplaySideButtons(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "Create")
    def test_instructorLoadUserButtons(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["UserButtons"], [])

    def test_instructorDisplayUserButtons(self):
        self.client.force_login(self.Instructor)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "Delete")
    def test_taLoadSideButtons(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")

        self.assertEqual(r.context["SideButtons"], [])

    def test_taLoadUserButtons(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["UserButtons"], [])
    def test_taDisplaySideButtons(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "Create")

    def test_taDisplayUserButtons(self):
        self.client.force_login(self.TA)
        r=self.client.get("/accountmanagement/")
        self.assertNotContains(r, "Delete")

    def test_adminLoadSideButtons(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["SideButtons"][0].value , "Create")
    def test_adminLoadSideButtons(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "Create")
    def test_adminLoadUserButtons(self):
        r=self.client.get("/accountmanagement/")
        self.assertEqual(r.context["UserButtons"][0].value, "Delete" )
    def test_adminDisplayUserButtons(self):
        r=self.client.get("/accountmanagement/")
        self.assertContains(r, "Delete")

class TestAccountCreationPost(TestCase):

    def setUp(self):
        self.client=Client()
        self.admin_group, created = Group.objects.get_or_create(name="manager")
        self.ta, created = Group.objects.get_or_create(name="ta")
        self.ta, created = Group.objects.get_or_create(name="instructor")
        newUser=User.objects.create_user(username="logged in larry", password="larryspassword")
        newUser.save()
        newUser.groups.add(self.admin_group)
        self.client.force_login(newUser)
        self.r=self.client.post("/accountmanagement/", {"username":"Testing123", "password":"sword1", "email":"testing@gmail.com", "name":"Manager Marcus", "altemail":"marcus@gmail.com", "phone":"999-999-9999", "address":"9999"}, follow=True)

    def test_newAccount(self):
        self.assertEqual(len(User.objects.all()),2)

    def test_newProfile(self):
        self.assertEqual(len(Profile.objects.all()),1)

    def test_displayNewAccountName(self):
        self.assertContains(self.r ,'Manager Marcus')

    def test_displayNewAccountEmail(self):
        self.assertContains(self.r, 'testing@gmail.com')

    def test_usernameStored(self):
        self.assertEqual(User.objects.all()[1].username, "Testing123")

    def test_emailStored(self):
        self.assertEqual(User.objects.all()[1].email,"testing@gmail.com")

    def test_passwordStored(self):
        self.assertNotEqual(User.objects.all()[0].password, None)

    def test_nameStored(self):
        self.assertEqual(User.objects.all()[1].first_name, "Manager Marcus")


    def test_userGroup(self):
        self.assertEqual(User.objects.all()[1].groups.all()[0].name,'manager')

    def test_altEmailStored(self):
        self.assertEqual(Profile.objects.all()[0].alt_email, "marcus@gmail.com")
    def test_altEmailDisplayed(self):
        self.assertContains(self.r, 'marcus@gmail.com')
    def test_phoneStored(self):
        self.assertEqual(Profile.objects.all()[0].phone, "999-999-9999")
    def test_phoneDisplayed(self):
        self.assertContains(self.r, "999-999-9999")
    def test_addressStored(self):
        self.assertEqual(Profile.objects.all()[0].address, "9999")
    def test_addressDisplayed(self):
        self.assertContains(self.r, "9999")
    def test_profileUser(self):
        self.assertEqual(Profile.objects.all()[0].user, User.objects.all()[1])
    def test_secondNewAccount(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertEqual(len(User.objects.all()) , 3)
    def test_secondNewAccountUser(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertEqual(User.objects.all()[2].username, "Testing1234")


    def test_secondNewAccountEmail(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertEqual(User.objects.all()[2].email, "testing4@gmail.com")

    def test_secondNewAccountName(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria","phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertEqual(User.objects.all()[2].first_name, "Manager Maria")

    def test_secondAccountPassword(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertNotEqual(User.objects.all()[1].password, None)


    def test_secondNewAccountGroup(self):
        self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)

        self.assertEqual(User.objects.all()[1].groups.all()[0].name, 'manager')




    def test_displaySecondNewAccountName(self):
        r=self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertContains(r, 'Manager Maria')

    def test_displaySecondNewAccountEmail(self):
        r=self.client.post("/accountmanagement/", {"username":"Testing1234", "password":"shield1", "email":"testing4@gmail.com", "name":"Manager Maria", "phone":"999-999-9998", "address":"9998", "altemail":"maria@gmail.com"}, follow=True)
        self.assertContains(r, 'testing4@gmail.com')


    def test_duplicateUserName(self):
        self.client.post("/accountmanagement/", {"name":"New Guy", "username":"Testing123", "password":"shield1", "email":"testing4@gmail.com", "address":"9998", "phone":"999-999-9998", "altemail":"alt99" }, follow=True)
        self.assertEqual(len(User.objects.all()),2)

    def test_duplicateUserNameKeepEmail(self):
        self.client.post("/accountmanagement/", {"name":"New Guy", "username":"Testing123", "password":"shield1", "email":"testing4@gmail.com", "address":"9998", "phone":"999-999-9998", "altemail":"alt99"}, follow=True)
        self.assertEqual(User.objects.all()[1].email, "testing@gmail.com")

    def test_duplicatePassword(self):
        self.client.post("/accountmanagement/", {"name":"New Guy", "username":"Testing1234", "password":"sword1", "email":"testing4@gmail.com","address":"9998", "phone":"999-999-9998", "altemail":"alt99" }, follow=True)
        self.assertEqual(len(User.objects.all()),3)

    #entering same username and password when creating a geniuenly new account
    def test_duplicateUserandPassword(self):
        self.client.post("/accountmanagement/", {"name":"New Guy", "username":"shield1", "password":"shield1", "email":"testing4@gmail.com", "address":"9998", "phone":"999-999-9998", "altemail":"alt99"}, follow=True)
        self.assertEqual(len(User.objects.all()), 3)

    def test_passwordHashed(self):
        self.assertNotEqual(User.objects.all()[0].password, "sword1")

    #Need to figure out exactly what duplicates are allowed, other than that, this has my thumbs up!