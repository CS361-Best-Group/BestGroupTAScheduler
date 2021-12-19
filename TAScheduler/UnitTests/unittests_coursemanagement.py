from django.test import TestCase
from django.contrib.auth.models import User, Group
from TAScheduler.models import Course, Section
from TAScheduler.views import CourseManagement
from ..apps import TASchedulerAppConfig

class TestLoad(TestCase):
    def setUp(self):
        TASchedulerAppConfig.ready(None)
        
        self.ta = User.objects.create_user('jsmith', 'jsmith@example.edu', '123')
        taGroup = Group.objects.get(name = 'ta')
        taGroup.user_set.add(self.ta)
        
        self.instructor = User.objects.create_user('awest', 'awest@example.edu', '456')
        instructorGroup = Group.objects.get(name = 'instructor')
        instructorGroup.user_set.add(self.instructor)
        
        self.manager = User.objects.create_user('bward', 'bward@example.edu', '789')
        managerGroup = Group.objects.get(name = 'manager')
        managerGroup.user_set.add(self.manager)
        
        self.other = User.objects.create_user('cromero', 'cromero@example.edu', '321')
        
        courseLayout = {
            'CS337': [
                'System Programming',
                [ self.instructor ],
                {
                    '301': [ self.ta ],
                    '302': [],
                }
            ],
            'CS594': [
                'Capstone Project Prep',
                [ self.ta, self.instructor ],
                {
                    '201': [],
                }
            ],
            'CS361': [
                'Introduction to Software Engineering',
                [ ],
                {
                    '451': [],
                }
            ]
        }
        
        for courseName, details in courseLayout.items():
            course = Course.objects.create(name = courseName, description = details[0])
            course.users.set(details[1])
            
            for sectionName, sectionUsers in details[2].items():
                section = Section.objects.create(name = sectionName, course = course)
                section.users.set(sectionUsers)
    
    def test_ta(self):
        courses, sections = CourseManagement.load(self.ta)
        
        taCourses = list(Course.objects.filter(users__in = [ self.ta ]))
        taSections = list(Section.objects.filter(users__in = [ self.ta ]))
        for section in taSections:
                if section.course not in taCourses:
                    taCourses.append(section.course)
        
        self.assertEqual(courses, taCourses)
        self.assertEqual(sections, taSections)
        
    def test_instructor(self):
        courses, sections = CourseManagement.load(self.instructor)
        
        instructorCourses = list(Course.objects.filter(users__in = [ self.instructor ]))
        instructorSections = list(Section.objects.filter(users__in = [ self.instructor ]) | Section.objects.filter(course__in = instructorCourses))
        
        self.assertEqual(courses, instructorCourses)
        self.assertEqual(sections, instructorSections)
        
    def test_manager(self):
        courses, sections = CourseManagement.load(self.manager)

        managerCourses = list(Course.objects.all())
        managerSections = list(Section.objects.all())
        
        self.assertEqual(courses, managerCourses)
        self.assertEqual(sections, managerSections)
    
    def test_other(self):
        courses, sections = CourseManagement.load(self.other)
        
        self.assertEqual(courses, [])
        self.assertEqual(sections, [])

class TestCreateCourse(TestCase):
    def test_create(self):
        CourseManagement.createCourse({ 'course': 'CS361', 'description': 'Introduction to Software Engineering' })
        Course.objects.get(name = 'CS361')
    
    def test_without_desc(self):
        CourseManagement.createCourse({ 'course': 'CS999', 'description': '' })
        newCourse = Course.objects.get(name = 'CS999')
        self.assertEqual(newCourse.description, 'No description')
    
    def test_without_name(self):
        CourseManagement.createCourse({ 'course': '', 'description': '' })
        self.assertEqual(list(Course.objects.all()), [])
    
    def test_invalid(self):
        CourseManagement.createCourse({})
        self.assertEqual(list(Course.objects.all()), [])

class TestCreateSection(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name = 'CS361', description = 'Introduction to Software Engineering')
        self.course.users.set([])
    
    def test_create(self):
        CourseManagement.createSection({ 'course': 'CS361', 'section': '301' })
        newSection = Section.objects.get(name = '301')
        self.assertEqual(newSection.course, self.course)
    
    def test_without_name(self):
        CourseManagement.createSection({ 'course': 'CS999', 'section': '' })
        self.assertEqual(list(Section.objects.all()), [])
    
    def test_without_course(self):
        CourseManagement.createSection({ 'course': '', 'section': '301' })
        
    def test_invalid_course(self):
        CourseManagement.createSection({ 'course': 'CS999', 'section': '301' })
        self.assertEqual(list(Section.objects.all()), [])
    
    def test_invalid(self):
        CourseManagement.createSection({})
        self.assertEqual(list(Section.objects.all()), [])

class TestDeleteCourse(TestCase):
    def setUp(self):
        course = Course.objects.create(name = 'CS999', description = 'Example course')
        Section.objects.create(name = 'ABC', course = course)
        
    def test_delete(self):
        CourseManagement.deleteCourse({ 'course': 'CS999' })
        self.assertEqual(list(Course.objects.all()), [])
        self.assertEqual(list(Section.objects.all()), [])
        
    def test_invalid(self):
        CourseManagement.deleteCourse({ 'course': '' })
        self.assertNotEqual(list(Course.objects.all()), [])
        self.assertNotEqual(list(Section.objects.all()), [])

class TestDeleteSection(TestCase):
    def setUp(self):
        course = Course.objects.create(name = 'CS999', description = 'Example course')
        Section.objects.create(name = 'ABC', course = course)
        
    def test_delete(self):
        CourseManagement.deleteCourse({ 'course': 'CS999', 'section': 'ABC' })
        self.assertEqual(list(Section.objects.all()), [])
        
    def test_invalid(self):
        CourseManagement.deleteCourse({ 'section': '' })
        self.assertNotEqual(list(Section.objects.all()), [])
