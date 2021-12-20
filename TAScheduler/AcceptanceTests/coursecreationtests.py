from django.db.models import QuerySet
from django.test import TestCase
from django.test import Client

from TAScheduler.apps import TASchedulerAppConfig
from TAScheduler.models import Course, Section, Profile
from django.contrib.auth.models import User, Group


class TestCourseCreationGet(TestCase):

    def setUp(self):
        TASchedulerAppConfig.ready(None)

        self.client=Client()
        self.dummy=User.objects.create_user(username="dummy23", password="password", email="email@email.com", first_name="dummy")
        self.dummy.save()

        self.TA=User.objects.create_user(username="TA23", password="password", email="ta@gmail.com", first_name="TA")
        self.TA.save()

        self.Course1=Course(name="CS361", description="Neat")
        self.Course1.save()

        self.Course1.users.set([self.dummy])
        #self.Section1=Section(name="CS361-001", course=self.Course1, users=[self.TA])
        self.Section1=Section(name="CS361-001", course=self.Course1)
        self.Section1.save()
        #self.Section1.course=self.Course1
        self.Section1.users.set([self.TA])
        self.Section1.save()


        self.dummy.groups.add(Group.objects.filter(name="manager")[0])
        self.dummy.save()
        self.client.force_login(self.dummy)
        self.r=self.client.get("/coursemanagement/")


    def test_loadCourseName(self):
        self.assertEqual(self.r.context["Courses"][0].name, "CS361")

    def test_displayCourseName(self):
        self.assertContains(self.r, 'CS361')

    def test_loadCourseDescription(self):
        self.assertEqual(self.r.context["Courses"][0].description, "Neat")

    def test_displayCourseDescription(self):
        self.assertContains(self.r, 'Neat')

    def test_loadCourseUser(self):
        self.assertEqual(self.r.context["Courses"][0].users.all()[0].first_name, "dummy")

    def test_displayCourseUser(self):
        self.assertContains(self.r, "dummy")

    def test_loadCourseSectionsName(self):
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].name, self.Section1.name)

    def test_displayCourseSectionsName(self):
        self.assertContains(self.r, "CS361-001")

    def test_loadSectionUser(self):
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].users.all()[0].first_name, "TA")

    def test_displaySectionUser(self):
        self.assertContains(self.r, "TA")


    ###########################################END LOAD/DISPLAY BASIC ELEMENTS #####################


    def test_loadMultipleCourseName(self):
        dummy2=User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2=User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2=Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()
        Section2=Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
        #Section2.course=Course2
        Section2.save()

        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].name, "CS 423")

    def test_displayMultipleCourseName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()
        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
#        Section2.course=Course2
        Section2.save()

        r=self.client.get("/coursemanagement/")
        self.assertContains(r, 'CS 423')
    def test_loadMultipleCourseDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()

        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
#        Section2.course=Course2
        r = self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].description, "also neat")

    def test_displayMultipleCourseDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()

        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
#        Section2.course=Course2
        Section2.save()


        r=self.client.get("/coursemanagement/")
        self.assertContains(r, "also neat")

    def test_loadMultipleCourseUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()

        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
#        Section2.users.set([TA2])
        Section2.course=Course2
        Section2.save()


        r=self.client.get("/coursemanagement/")


        self.assertEqual(r.context["Courses"][0].users.all()[0].first_name, "dummy2")

    def test_displayMultipleCourseUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()

        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()

        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()
        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
#        Section2.course=Course2
        Section2.save()

        r=self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy2")

    def test_loadMultipleCourseSectionsName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()



        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
#        Section2.course=Course2
        Section2.users.set([TA2])
        Section2.save()
        r = self.client.get("/coursemanagement/")

        self.assertEqual(Section.objects.filter(course=Course2)[0].name, "CS423-001")

    def test_displayMultipleCourseSectionsName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()
        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
        Section2.course=Course2
        Section2.save()

        r=self.client.get("/coursemanagement/")

        self.assertContains(r, "CS423-001")
    #users of the section is what is being tested here
    def test_loadMultipleCourseSectionsUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()

        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
#        Section2.course=Course2
        Section2.save()


        r = self.client.get("/coursemanagement/")

        self.assertEqual(Section.objects.filter(course=Course2)[0].users.all()[0].first_name, "TA2")

    def test_displayMultipleCourseSectionUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw1rd", email="email2@gmail.com", first_name="dummy2")
        dummy2.save()
        TA2 = User.objects.create_user(username="TA221", password="passw0rd", email="email3@gmail.com", first_name="TA2")
        TA2.save()
        Course2 = Course(name="CS 423", description="also neat")
        Course2.save()
        Course2.users.set([dummy2])
        Course2.save()
        Section2 = Section(name="CS423-001", course=Course2)
        Section2.save()
        Section2.users.set([TA2])
#        Section2.course=Course2
        Section2.save()

        r=self.client.get("/coursemanagement/")
        self.assertContains(r, "TA2")


####################################END MULTIPLE COURSE TESTS##########################################

    def test_loadNoUsersName(self):
        self.Course1.users.set([])
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].name, "CS361")

    def test_displayNoUsersName(self):
        self.Course1.users.set([])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, 'CS361')
    def test_loadNoUsersDescription(self):
        self.Course1.users.set([])
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].description, "Neat")
    def test_displayNoUsersDescription(self):
        self.Course1.users.set([])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Neat")
    def test_loadNoUsersSectionName(self):
        self.Course1.users.set([])
        r=self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].name, "CS361-001")
    def test_displayNoUsersSectionName(self):
        self.Course1.users.set([])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "CS361-001")
    def test_loadNoUsersSectionUsers(self):
        self.Course1.users.set([])
        r=self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].users.all()[0].first_name, "TA")

    def test_displayNoUsersSectionsUsers(self):
        self.Course1.users.set([])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "TA")


#############################################END NO USERS TESTS ################################################



    def test_loadCourseMultipleUsers(self):
        dummy2=User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()

        r=self.client.get("/coursemanagement/")

        self.assertEqual(list(r.context["Courses"][0].users.all()), [self.dummy, dummy2])

    def test_displayCourseMultipleUsers1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy")

    def test_displayCourseMultipleUsers2(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy2")
    def test_loadCourseMultipleUsersName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].name, "CS361")

    def test_displayCourseMultipleUsersName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, 'CS361')

    def test_loadCoursesMultipleUsersDescription(self):
        dummy2=User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].description, "Neat")

    def test_displayCourseMultipleUsersDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Neat")


    def test_loadCoursesMultipleUsersSectionName(self):
        dummy2=User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()

        r=self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].name, "CS361-001")

    def test_displayCoursesMultipleUsersSectionName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")

        self.assertContains(r, "CS361-001")

    def test_loadCoursesMultipleUsersSectionUsers(self):
        dummy2=User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r=self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].users.all()[0].first_name, "TA")

    def test_displayCoursesMultipleUsersSectionUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()
        self.Course1.users.set([self.dummy, dummy2])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")

        self.assertContains(r, "TA")


    ##################################END SINGLE COURSE MULTIPLE USER TESTS########################################


    def test_loadCourseMultipleSectionsName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2=Section(name="CS361-002", course=self.Course1)
        Section2.save()
        #Section2.course=self.Course1
        Section2.users.set([dummy2])
        Section2.save()
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].name, "CS361")

    def test_displayCourseMultipleSectionSName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, 'CS361')

    def test_loadCourseMultipleSectionsUser(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2=Section(name="CS361-002", course=self.Course1)
        Section2.save()
#        Section2.course=self.Course1
        Section2.users.set([dummy2])
        Section2.save()

        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].users.all()[0].first_name,"dummy")

    def test_displayCourseMultipleSectionsUser(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy")
    def test_loadCourseMultipleSectionsDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2=Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()

        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].description, "Neat")

    def test_displayCourseMultipleSectionsDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1

        Section2.save()

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Neat")
    def test_loadCourseMultipleSectionsSections(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2=Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()



        r=self.client.get("/coursemanagement/")
        self.assertEqual(list(Section.objects.filter(course=self.Course1)), [self.Section1, Section2])

    def test_displayCourseMultipleSectionsSections(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "CS361-002")
    def test_loadCourseMultipleSectionsUser1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2=Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()


        r=self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].users.all()[0].first_name, "TA")

    def test_displayCourseMultipleSectionsUser1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1

        Section2.save()

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "TA")
    def test_loadCourseMultipleSectionUser2(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2=Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
        #Section2.course=self.Course1
        Section2.save()
        r=self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[1].users.all()[0].first_name, "dummy2")

    def test_displayCourseMultipleSectionUser2(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
        #Section2.course=self.Course1
        Section2.save()
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy2")


#########################################END COURSES WITH MULTIPLE SECTIONS TESTS############################
#########################################BEGIN COURSES WITH MULTIPLE USERS AND SECTIONS TESTS###############



    def test_loadCourseMultipleUsersSectionsName(self):

        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail", first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        self.Course1.save()
        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].name, "CS361")

    def test_displayCourseMultipleUsersSectionsName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course=self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail", first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, 'CS361')


    def test_loadCoursesMultipleUsersSectionsDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()


        self.Course1.users.set([self.dummy, dummy3])

        r = self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].description, "Neat")

    def test_displayCourseMultipleUsersSectionsDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail", first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Neat")

    def test_loadCoursesMultipleUsersSectionsUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy,dummy3])
        self.Course1.save()

        r = self.client.get("/coursemanagement/")


        self.assertEqual(list(r.context["Courses"][0].users.all()), [self.dummy, dummy3])
    #Sections with multiple users

    def test_displayCoursesMultipleUsersSectionsUsers1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
#        Section2.save()
        Section2.users.set([dummy2])
        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy")

    def test_displayCoursesMultipleUsersSectionsUsers2(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
        #Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy3")


    def test_loadCourseMultipleUsersSectionsSections(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()


        self.Course1.users.set([self.dummy, dummy3])
        self.Course1.save()
        r = self.client.get("/coursemanagement/")
        self.assertEqual(list(Section.objects.filter(course=self.Course1)), [self.Section1, Section2])

    def test_displayCourseMultipleUsersSectionsSections1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "CS361-001")


    def test_displayCourseMultipleUsersSectionsSections2(self):
        dummy2 = User.objects.create_user(username="dummy298", password="passw0rd", email="email2", first_name="dummy2")
        dummy2.save()

        Section2 = Section(name="CS361-002", course=self.Course1)
        Section2.save()
        Section2.users.set([dummy2])
#        Section2.course = self.Course1
        Section2.save()

        dummy3 = User.objects.create_user(username="dummy321", password="password", email="noemail",first_name="dummy3")
        dummy3.save()

        self.Course1.users.set([self.dummy, dummy3])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "CS361-002")

    #################################END COURSE WITH MULTIPLE SECTIONS AND USERS TESTING####################
    #################################Begin course with multiple users in a section testing###################

    def test_loadCourseSectionMultipleUsersName(self):
        dummy2=User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()
        self.Section1.users.set([self.TA, dummy2])


        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].name, "CS361")

    def test_displayCourseSectionMultipleUsersName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()


        self.Section1.users.set([self.TA, dummy2])

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, 'CS361')

    def test_loadCourseSectionMultipleUsersDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()


        self.Section1.users.set([self.TA, dummy2])

        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].description, "Neat")

    def test_displayCourseSectionMultipleUsersDescription(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()
        self.Section1.users.set([self.TA, dummy2])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Neat")
    def test_loadCourseSectionMultipleUsersUser(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()


        self.Section1.users.set([self.TA, dummy2])

        r=self.client.get("/coursemanagement/")
        self.assertEqual(r.context["Courses"][0].users.all()[0].first_name, "dummy")

    def test_displayCourseSectionMultipleUsersUser(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()
        self.Section1.users.set([self.TA, dummy2])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy")
    def test_loadCoursesSectionMultipleUsersSectionName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()
        self.Section1.users.set([self.TA, dummy2])
        self.client.get("/coursemanagement/")
        self.assertEqual(Section.objects.filter(course=self.Course1)[0].name, "CS361-001")
    def test_displayCoursesSectionMultipleUsersSectionName(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()

        self.Section1.users.set([self.TA, dummy2])

        r = self.client.get("/coursemanagement/")
        self.assertContains(r,"CS361-001")
    def test_loadCourseSectionMultipleUsersSectionUsers(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()

        self.Section1.users.set([self.TA, dummy2])

        self.client.get("/coursemanagemement/")
        self.assertEqual(list(Section.objects.filter(course=self.Course1)[0].users.all()), [self.TA, dummy2])
    def test_displayCourseSectionMultipleUsersSectionUsers1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()
        self.Section1.users.set([self.TA, dummy2])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "TA")
    def test_displayCourseSectionMultipleUsersSectionUsers1(self):
        dummy2 = User.objects.create_user(username="dummy298", password="password", email="email23", first_name="dummy2")
        dummy2.save()
        self.Section1.users.set([self.TA, dummy2])
        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "dummy2")


    def test_adminDisplayAssignCourse(self):
        Admin=User.objects.create_user(username="Admin", password="Admin", email="admin@gmail.com", first_name="Admin Adam")
        Admin.save()
        AdminProfile=Profile(user=Admin, address="2345", phone="144-412-4124", alt_email="alternateadmin@gmail.com")
        AdminProfile.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        Admin.save()
        self.client.force_login(Admin)

        r=self.client.get("/coursemanagement/")
        self.assertContains(r, "Assign User To Course")

    def test_adminDisplayAssignSection(self):
        Admin = User.objects.create_user(username="Admin", password="Admin", email="admin@gmail.com",                                         first_name="Admin Adam")
        Admin.save()
        AdminProfile = Profile(user=Admin, address="2345", phone="144-412-4124", alt_email="alternateadmin@gmail.com")
        AdminProfile.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        Admin.save()
        self.client.force_login(Admin)

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Assign User To Section")

    def test_adminDisplayCreateCourse(self):
        Admin = User.objects.create_user(username="Admin", password="Admin", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        AdminProfile = Profile(user=Admin, address="2345", phone="144-412-4124", alt_email="alternateadmin@gmail.com")
        AdminProfile.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        Admin.save()
        self.client.force_login(Admin)

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Create")

    def test_adminDisplayDeleteCourse(self):
        Admin = User.objects.create_user(username="Admin", password="Admin", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        AdminProfile = Profile(user=Admin, address="2345", phone="144-412-4124", alt_email="alternateadmin@gmail.com")
        AdminProfile.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        Admin.save()
        self.client.force_login(Admin)

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Delete Course")

    def test_adminCreateSection(self):
        Admin = User.objects.create_user(username="Admin", password="Admin", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        AdminProfile = Profile(user=Admin, address="2345", phone="144-412-4124", alt_email="alternateadmin@gmail.com")
        AdminProfile.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        Admin.save()
        self.client.force_login(Admin)

        r = self.client.get("/coursemanagement/")
        self.assertContains(r, "Create Section")

    def test_taNoAssignCourse(self):
        TA= User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com", skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()
        self.client.force_login(TA)

        r=self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Assign User To Course")

    def test_taNoAssignSection(self):
        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()
        self.client.force_login(TA)

        r = self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Assign User To Section")
    def test_taNoCreateCourse(self):
        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()
        self.client.force_login(TA)

        r = self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Create")

    def test_taNoDeleteCourse(self):
        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()
        self.client.force_login(TA)

        r = self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Delete Course")
    def test_taNoCreateSection(self):
        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()
        self.client.force_login(TA)

        r = self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Create Section")

    def test_instructorNoAssignCourse(self):
        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor.groups.add(Group.objects.filter(name="instructor")[0])
        Instructor.save()
        self.client.force_login(Instructor)

        r=self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Assign User To Course")
    def test_instructorAssignSection(self):
        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()
        self.Course1.users.set([Instructor])
        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor.groups.add(Group.objects.filter(name="instructor")[0])
        Instructor.save()
        self.client.force_login(Instructor)

        r=self.client.get("/coursemanagement/")
        self.assertContains(r, "Assign User To Section")

    def test_instructorNoCreateCourse(self):
        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor.groups.add(Group.objects.filter(name="instructor")[0])
        Instructor.save()
        self.client.force_login(Instructor)

        r=self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Create")
    def test_instructorNoDeleteCourse(self):
        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor.groups.add(Group.objects.filter(name="instructor")[0])
        Instructor.save()
        self.client.force_login(Instructor)

        r=self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Delete Course")
    def test_instructorNoCreateSection(self):
        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor.groups.add(Group.objects.filter(name="instructor")[0])
        Instructor.save()
        self.client.force_login(Instructor)

        r=self.client.get("/coursemanagement/")
        self.assertNotContains(r, "Create Section")
























class TestCourseCreationPost(TestCase):

    def setUp(self):
        self.client=Client()
        TASchedulerAppConfig.ready(None)

        self.dummy=User.objects.create_user(username="dummy23", password="password", email="email@email.com", first_name="dummy")
        self.dummy.save()
        self.dummy.groups.add(Group.objects.filter(name="manager")[0])
        
        self.client.force_login(self.dummy)

    def test_sectionCreation(self):
        Course1=Course(name="CS361", description="neat")
        Course1.save()

        self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertEqual(len(Section.objects.all()),1)

    def test_courseCreation(self):

        self.client.post("/coursemanagement/", {"coursename":"CS361", "coursedescription":"neat"}, follow=True)

        self.assertEqual(len(Course.objects.all()),1)

    def test_courseCreationName(self):
        self.client.post("/coursemanagement/", {"coursename": "CS361", "coursedescription": "neat"}, follow=True)
        self.assertEqual(Course.objects.all()[0].name, "CS361")

    def test_courseCreationUsers(self):
        self.client.post("/coursemanagement/", {"coursename": "CS361", "coursedescription": "neat"}, follow=True)
        self.assertEqual(len(Course.objects.all()[0].users.all()),0)

    def test_courseCreationSections(self):
        self.client.post("/coursemanagement/", {"coursename": "CS361", "coursedescription": "neat"}, follow=True)
        newcourse=Course.objects.filter(name="CS361")[0]
        self.assertEqual(len(Section.objects.filter(course=newcourse)), 0)

    def test_courseCreationDescription(self):
        self.client.post("/coursemanagement/", {"coursename":"CS361", "coursedescription":"neat"}, follow=True)
        self.assertEqual(Course.objects.all()[0].description, "neat")

    def test_sectionCreationName(self):
        Course1=Course(name="CS361", description="neat")
        Course1.save()

        self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertEqual(Section.objects.all()[0].name, "CS361-001")

    def test_sectionCreationUser(self):
        Course1=Course(name="CS361", description="neat")
        Course1.save()
        self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertEqual(len(Section.objects.all()[0].users.all()),0)

    def test_sectionCreationCourse(self):
        Course1=Course(name="CS361", description="neat")
        Course1.save()
        self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertEqual(Section.objects.all()[0].course, Course1)


    def test_displaySectionName(self):
        Course1=Course(name="CS361", description="neat")
        Course1.save()
        r=self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertContains(r, "CS361-001")

    def test_displayCourseName(self):
        r=self.client.post("/coursemanagement/", {"coursename":"CS361", "coursedescription":"Neat"}, follow=True)
        self.assertContains(r, 'CS361')

    def test_displayCourseDescription(self):
        r=self.client.post("/coursemanagement/", {"coursename":"CS361", "coursedescription":"Neat"}, follow=True)
        self.assertContains(r, "Neat")

    def test_secondNewCourse(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r=self.client.post("/coursemanagement/", {"coursename":"CS423", "coursedescription":"Also neat"}, follow=True)
        self.assertEqual(len(Course.objects.all()),2)
    def test_secondNewCourseName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r=self.client.post("/coursemanagement/", {"coursename":"CS423", "coursedescription":"Also neat"}, follow=True)
        self.assertEqual(Course.objects.all()[1].name, "CS423")

    def test_displaysecondNewCourseName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r = self.client.post("/coursemanagement/", {"coursename": "CS423", "coursedescription": "Also neat"},follow=True)
        self.assertContains(r, 'CS423')

    def test_secondNewCourseDescription(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r = self.client.post("/coursemanagement/", {"coursename": "CS423", "coursedescription": "Also neat"},follow=True)
        self.assertEqual(Course.objects.all()[1].description, "Also neat")

    def test_displaysecondNewCourseDescription(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r = self.client.post("/coursemanagement/", {"coursename": "CS423", "coursedescription": "Also neat"},follow=True)
        self.assertContains(r, "Also neat")

    def test_secondNewCourseUsers(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r = self.client.post("/coursemanagement/", {"coursename": "CS423", "coursedescription": "Also neat"},follow=True)
        self.assertEqual(len(Course.objects.all()[1].users.all()), 0)

    def test_secondNewCourseSections(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        r = self.client.post("/coursemanagement/", {"coursename": "CS423", "coursedescription": "Also neat"},follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course1)),0)


    def test_secondNewSection(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Section1 = Section(name="CS361-001", course=Course1)
        Section1.save()
        Section1.users.set([])
#        Section1.course = Course1
        Section1.save()

        self.client.post("/coursemanagement/", {"course": "CS361"}, follow=True)
        self.assertEqual(len(Section.objects.all()),2)

    def test_secondNewSectionName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Section1 = Section(name="CS361-001", course=Course1)
        Section1.save()
        Section1.users.set([])
#        Section1.course=Course1
        Section1.save()

        self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertEqual(Section.objects.all()[1].name, "CS361-002")
    def test_displaySecondNewSectionName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Section1 = Section(name="CS361-001", course=Course1)
        Section1.save()
        Section1.users.set([])
#        Section1.course = Course1
        Section1.save()
        r=self.client.post("/coursemanagement/", {"course":"CS361"}, follow=True)
        self.assertContains(r, "CS361-002")


    def test_secondNewSectionUsers(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Section1 = Section(name="CS361-001", course=Course1)
        Section1.save()
        Section1.users.set([])
        Section1.course = Course1
        Section1.save()

        self.client.post("/coursemanagement/", {"course": "CS361"}, follow=True)
        self.assertEqual(len(Section.objects.all()[1].users.all()),0)

    def test_secondNewSectionCourse(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Section1 = Section(name="CS361-001", course=Course1)
        Section1.save()
        Section1.users.set([])
#        Section1.course = Course1
        Section1.save()

        self.client.post("/coursemanagement/", {"course": "CS361"}, follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course1)),2)



    def test_courseCreationNoInput(self):
        self.client.post("/coursemanagement/", {"coursename":"", "coursedescription":""}, follow=True)
        self.assertEqual(len(Course.objects.all()),0)

    def test_courseCreationNoDescription(self):
        self.client.post("/coursemanagement/", {"coursename":"CS423", "coursedescription":""}, follow=True)
        self.assertEqual(len(Course.objects.all()), 0)

    def test_courseCreationNoName(self):
        self.client.post("/coursemanagement/", {"coursename":"", "coursedescription":"Also neat"}, follow=True)
        self.assertEqual(len(Course.objects.all()), 0)


    #Adding second section to a second course

    def test_secondCourseSecondSectionCourse1(self):
        Course1=Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2=Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11=Section(name="CS361-001", course=Course1)
        Section11.save()
#        Section11.course=Course1
        Section11.users.set([])
        Section11.save()


        Section12=Section(name="CS361-002", course=Course1)
        Section12.save()
#        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21=Section(name="CS423-001", course=Course2)
        Section21.save()
#        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course":"CS423"}, follow=True)

        self.assertEqual(len(Section.objects.filter(course=Course1)),2)


    def test_secondCourseSecondSectionCourse2(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course2)),2)




    def test_secondCourseSecondSectionCourse1Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(Course1.name, "CS361")

    def test_displaysecondCourseSecondSectionCourse1Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r = self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, 'CS361')

    def test_secondCourseSecondSectionCourse2Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(Course2.name, "CS423")

    def test_displaySecondCourseSecondSectionCourse2Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r = self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, 'CS423')

    def test_secondCourseSecondSectionCourse1Description(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(Course1.description, "neat")
    def test_displaySecondCourseSecondSectionCourse1Description(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r=self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, "neat")
    def test_secondCourseSecondSectionCourse2Description(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()


        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(Course2.description, "Also neat")

    def test_displaySecondCourseSecondSectionCourse2Description(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r=self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, "Also neat")
    def test_secondCourseSecondSectionCourse1Users(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Course.objects.all()[0].users.all()),0)
    def test_secondCourseSecondSectionCourse2Users(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Course.objects.all()[1].users.all()),0)

    def test_secondCourseSecondSectionCourse1Section1Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(Section.objects.filter(course=Course1)[0].name, "CS361-001")
    def test_displaySecondCourseSecondSectionCourse1Section1Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r=self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, "CS361-001")
    def test_secondCourseSecondSectionCourse2Section1Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course":"CS423"}, follow=True)
        self.assertEqual(Section.objects.filter(course=Course2)[0].name, "CS423-001")

    def test_displaySecondCourseSecondSectionCourse2Section1Name(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r=self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, "CS423-001")
    def test_secondCourseSecondSectionCourse1Section1Users(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course1)[1].users.all()),0)



    def test_secondCourseSecondSectionCourse2Section1Users(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course2)[0].users.all()), 0)
    def test_secondCourseSecondSectionCourse1SecondSectionName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertEqual(Section.objects.filter(course=Course1)[1].name, "CS361-002")

    def test_displaySecondCourseSecondSectionCourse1SecondSectionName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r=self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, "CS361-002")
    def test_secondCourseSecondSectionCourse2SecondSectionName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertEqual(Section.objects.filter(course=Course2)[1].name, "CS423-002")

    def test_displaySecondCourseSecondSectionCourse2SecondSectionName(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        r=self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertContains(r, "CS423-002")
    def test_secondCourseSecondSectionCourse1SecondSectionUsers(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagment/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course1)[1].users.all()), 0)
    def test_secondcourseSectionSectionCourse2SecondSectionUsers(self):
        Course1 = Course(name="CS361", description="neat")
        Course1.save()
        Course1.users.set([])

        Course2 = Course(name="CS423", description="Also neat")
        Course2.save()
        Course2.users.set([])

        Course1.save()
        Course2.save()

        Section11 = Section(name="CS361-001", course=Course1)
        Section11.save()
        #        Section11.course=Course1
        Section11.users.set([])
        Section11.save()

        Section12 = Section(name="CS361-002", course=Course1)
        Section12.save()
        #        Section12.course=Course1
        Section12.users.set([])
        Section12.save()

        Section21 = Section(name="CS423-001", course=Course2)
        Section21.save()
        #        Section21.course=Course2
        Section21.users.set([])
        Section21.save()

        self.client.post("/coursemanagement/", {"course": "CS423"}, follow=True)
        self.assertEqual(len(Section.objects.filter(course=Course2)[1].users.all()),0)

    def test_createDuplicateCourse(self):
        Course1=Course(name="CS361", description="A really neat course")
        Course1.save()
        Course1.users.set([])
        Course1.save()
        self.client.post("/coursemanagement/", {"coursename":"CS361", "coursedescription":"A really neat course"}, follow=True)
        self.assertEqual(len(Course.objects.all()),1)
    def test_createDuplicateCourseDescription(self):
        Course1 = Course(name="CS361", description="A really neat course")
        Course1.save()
        Course1.users.set([])
        Course1.save()
        self.client.post("/coursemanagement/", {"coursename": "CS361", "coursedescription": "A really cool course"},follow=True)
        self.assertEqual(Course.objects.all()[0].description, "A really neat course")
#duplicates also
    def test_assignInstructortoCourse(self):
        Admin=User.objects.create_user(username="Admin", password="password", email="admin@gmail.com", first_name="Admin Adam")
        Admin.save()
        Profile1=Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1=Course(name="CS361", description="neat")
        Course1.save()

        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()


        r=self.client.post("/coursemanagement/", {"user":"Instructor Isiah", "kind":"assignUser", "course":"CS361"})
        self.assertEqual(Course1.users.first().first_name,"Instructor Isiah")


    def test_assignTAtoCourse(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()


        r=self.client.post("/coursemanagement/", {"user":"TA Tobey", "kind":"assignUser", "course":"CS361"})
        self.assertEqual(Course1.users.first().first_name,"TA Tobey")


    def test_assignTAtoSection(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()

        Section1=Section(course=Course1, name="CS361-001")
        Section1.save()
        r=self.client.post("/coursemanagement/", {"user":"TA Tobey", "kind":"assignUser", "section":"CS361-001"})
        self.assertEqual(Section1.users.first().first_name,"TA Tobey")

    def test_assignSecondInstructorToCourse(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        Instructor = User.objects.create_user(username="Instructor", password="Instructor",
                                              email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile = Profile(user=Instructor, address="2413", phone="414-412-1351",
                                    alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor2 = User.objects.create_user(username="Instructor2", password="Instructor2",
                                              email="instructo2r@gmail.com", first_name="Instructor Isiah2")
        Instructor2.save()

        InstructorProfile2 = Profile(user=Instructor2, address="2413", phone="413-412-1351",
                                    alt_email="instructor2alternateemail.com")
        InstructorProfile2.save()

        self.client.post("/coursemanagement/", {"kind":"assignUser", "course":"CS361", "user":"Instructor Isiah2"})
        r=self.client.post("/coursemanagement/", {"user":"Instructor Isiah", "kind":"assignUser", "course":"CS361"})

        self.assertEqual(Course1.users.all()[1].first_name, "Instructor Isiah2")
    def test_assignSecondTAToSection(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()

        TA2 = User.objects.create_user(username="TA2", password="TA2", email="ta2@gmail.com", first_name="TA Maguire")
        TA2.save()
        TAProfile2 = Profile(user=TA2, address="3543", phone="154-142-4234", alt_email="taalternate2@gmail.com",
                            skills="Bully Maguire")
        TAProfile2.save()

        Section1 = Section(course=Course1, name="CS361-001")
        Section1.save()
        self.client.post("/coursemanagement/", {"user": "TA Tobey", "kind": "assignUser", "section": "CS361-001"})
        r=self.client.post("/coursemanagement/", {"user": "TA Maguire", "kind": "assignUser", "section": "CS361-001"})

        self.assertEqual(Section1.users.all()[1].first_name, "TA Maguire")
    def test_assignInstructorToSecondCourse(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        Course2= Course(name="CS423", description="also neat")
        Course2.save()

        Instructor = User.objects.create_user(username="Instructor", password="Instructor",
                                              email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile = Profile(user=Instructor, address="2413", phone="414-412-1351",
                                    alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        r = self.client.post("/coursemanagement/",
                             {"user": "Instructor Isiah", "kind": "assignUser", "course": "CS423"})
        self.assertEqual(Course2.users.first().first_name, "Instructor Isiah")

    def test_assignTAToSecondSection(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()



        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()

        Section1 = Section(course=Course1, name="CS423-001")
        Section1.save()
        Section2 = Section(course=Course1, name="CS423-002")
        Section2.save()
        r = self.client.post("/coursemanagement/", {"user": "TA Tobey", "kind": "assignUser", "section": "CS423-002"})
        self.assertEqual(Section2.users.first().first_name, "TA Tobey")

    def test_displayAssignedInstructor(self):
        Admin=User.objects.create_user(username="Admin", password="password", email="admin@gmail.com", first_name="Admin Adam")
        Admin.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        self.client.force_login(Admin)
        Profile1=Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1=Course(name="CS361", description="neat")
        Course1.save()

        Instructor = User.objects.create_user(username="Instructor", password="Instructor", email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile=Profile(user=Instructor, address="2413", phone="414-412-1351", alt_email="instructoralternateemail.com")
        InstructorProfile.save()


        r=self.client.post("/coursemanagement/", {"user":"Instructor Isiah", "kind":"assignUser", "course":"CS361"}, follow=True)
        self.assertContains(r, "Instructor Isiah")
    def test_displayAssignedTA(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        self.client.force_login(Admin)
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()

        Section1 = Section(course=Course1, name="CS361-001")
        Section1.save()
        r = self.client.post("/coursemanagement/", {"user": "TA Tobey", "kind": "assignUser", "section": "CS361-001"}, follow=True)
        self.assertContains(r, "TA Tobey")

    def test_displaySecondInstructor(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        self.client.force_login(Admin)
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        Instructor = User.objects.create_user(username="Instructor", password="Instructor",
                                              email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile = Profile(user=Instructor, address="2413", phone="414-412-1351",
                                    alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        Instructor2 = User.objects.create_user(username="Instructor2", password="Instructor2",
                                               email="instructo2r@gmail.com", first_name="Instructor Isiah2")
        Instructor2.save()

        InstructorProfile2 = Profile(user=Instructor2, address="2413", phone="413-412-1351",
                                     alt_email="instructor2alternateemail.com")
        InstructorProfile2.save()

        self.client.post("/coursemanagement/", {"kind": "assignUser", "course": "CS361", "user": "Instructor Isiah2"})
        r = self.client.post("/coursemanagement/",
                             {"user": "Instructor Isiah", "kind": "assignUser", "course": "CS361"}, follow=True)

        self.assertContains(r, "Instructor Isiah2")

    def test_displaySecondTA(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        self.client.force_login((Admin))
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()

        TA2 = User.objects.create_user(username="TA2", password="TA2", email="ta2@gmail.com", first_name="TA Maguire")
        TA2.save()
        TAProfile2 = Profile(user=TA2, address="3543", phone="154-142-4234", alt_email="taalternate2@gmail.com",
                             skills="Bully Maguire")
        TAProfile2.save()

        Section1 = Section(course=Course1, name="CS361-001")
        Section1.save()
        self.client.post("/coursemanagement/", {"user": "TA Tobey", "kind": "assignUser", "section": "CS361-001"})
        r = self.client.post("/coursemanagement/", {"user": "TA Maguire", "kind": "assignUser", "section": "CS361-001"}, follow=True)

        self.assertContains(r, "TA Maguire")

    def test_displaySecondCourseInstructor(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        self.client.force_login(Admin)
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        Course2 = Course(name="CS423", description="also neat")
        Course2.save()

        Instructor = User.objects.create_user(username="Instructor", password="Instructor",
                                              email="instructor@gmail.com", first_name="Instructor Isiah")
        Instructor.save()

        InstructorProfile = Profile(user=Instructor, address="2413", phone="414-412-1351",
                                    alt_email="instructoralternateemail.com")
        InstructorProfile.save()

        r = self.client.post("/coursemanagement/",
                             {"user": "Instructor Isiah", "kind": "assignUser", "course": "CS423"}, follow=True)
        self.assertContains(r, "Instructor Isiah")

    def test_displaySecondSectionTA(self):
        Admin = User.objects.create_user(username="Admin", password="password", email="admin@gmail.com",
                                         first_name="Admin Adam")
        Admin.save()
        Admin.groups.add(Group.objects.filter(name="manager")[0])
        self.client.force_login(Admin)
        Profile1 = Profile(user=Admin, address="9924", phone="412-412-4235", alt_email="alternateemail@gmail.com")
        Profile1.save()
        Course1 = Course(name="CS361", description="neat")
        Course1.save()

        TA = User.objects.create_user(username="TA", password="TA", email="ta@gmail.com", first_name="TA Tobey")
        TA.save()
        TAProfile = Profile(user=TA, address="3243", phone="151-142-4234", alt_email="taalternate@gmail.com",
                            skills="Cool Dude")
        TAProfile.save()
        TA.groups.add(Group.objects.filter(name="ta")[0])
        TA.save()

        Section1 = Section(course=Course1, name="CS423-001")
        Section1.save()
        Section2 = Section(course=Course1, name="CS423-002")
        Section2.save()
        r = self.client.post("/coursemanagement/", {"user": "TA Tobey", "kind": "assignUser", "section": "CS423-002"}, follow=True)
        self.assertContains(r, "TA Tobey")