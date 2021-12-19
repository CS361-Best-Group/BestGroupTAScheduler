from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group
from TAScheduler.models import Course, Section
from TAScheduler.apps import TASchedulerAppConfig

# As an administrator, I must be able to create courses within the system, in order to assign them to instructors and TAs.
class TestCourseCreationAcceptance(TestCase):
    def setUp(self):
        self.client = Client()
        
        TASchedulerAppConfig.ready(None)
        
        self.userA = User.objects.create_user('jsmith', 'jsmith@example.edu', '123')
        managerGroup = Group.objects.get(name = 'manager')
        
        # GIVEN my account has administrative privileges.
        managerGroup.user_set.add(self.userA)
        
        # AND I am currently logged into my account.
        self.client.force_login(self.userA)
    
    def testSuccessfulCourseCreation(self):
        # WHEN I submit a new course.
        response = self.client.post('/coursemanagement/', {'coursename': 'CS361', 'coursedescription': 'Introduction to Software Engineering'}, follow = True)
        # THEN the course information is validated by the system.
        
        # WHEN the course information is valid.
        
        # THEN the course is added to the database.
        newCourse = Course.objects.get(name='CS361')
        
        # AND I am redirected back to the course management page, which displays the new course.
        self.assertEqual(response.context.request.path, '/coursemanagement/')
        self.assertIn(newCourse, response.context['Courses'])


    def testUnsuccessfulCourseCreation(self):
        # WHEN I submit a new course.
        response = self.client.post('/coursemanagement/', {'coursename': '', 'coursedescription': ''}, follow = True)
        # THEN the course information is validated by the system.
        
        # WHEN the course information is invalid.
        
        # THEN I am redirected back to the course management page.
        # AND I am informed that the course information is invalid.
        self.assertEqual(response.context.request.path, '/coursemanagement/')
        self.assertEqual(list(response.context['Courses']), [])
    
    def testSectionCreation(self):
        # GIVEN the course already exists.
        course = Course.objects.create(name = 'CS361', description = 'Introduction to Software Engineering')
        
        # WHEN I press the 'add section' button associated with the course.
        response = self.client.post('/coursemanagement/', {'course': 'CS361'}, follow = True)
        
        # THEN the section is added to the database.
        newSection = Section.objects.get(name='CS361-001')
        
        # AND I am redirected back to the course management page, which displays the new section.
        self.assertEqual(response.context.request.path, '/coursemanagement/')
        self.assertIn(newSection, response.context['Sections'])
