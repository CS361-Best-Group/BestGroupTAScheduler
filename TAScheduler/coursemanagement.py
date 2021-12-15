from django.contrib.auth.models import User, Group
from TAScheduler.models import Course, Section

def handleForm(context):
    formHandlers = {
        'createCourse': createCourse,
        'createSection': createSection,
        'deleteCourse': deleteCourse,
        'deleteSection': deleteSection,
        'assignUser': assignUser
    }
    
    if 'kind' in context.keys():
        formHandlers.get(context['kind'], lambda *args, **keyArgs: None)(context)

def createCourse(context):
	# TODO: group membership check.
    name = context.get('course', '')

    if name != '' and len(Course.objects.filter(name = name)) == 0:
        description = context.get('description', 'No description')
        
        course = Course(name = name, description = description)
        course.users.set([])

        course.save()

def createSection(context):
	# TODO: group membership check.
	course = Course.objects.get(name = context.get('course', ''))
	
	if course is not None:
		name = context.get('section', '')
		
		if name != '' and len(Section.objects.filter(course = course, name = name)) == 0:
			section = Section(name = name, course = course)
			section.users.set([])
			section.save()

def deleteCourse(context):
    # To be implemented.
    pass

def deleteSection(context):
    # To be implemented.
    pass

def assignUser(context):
    # To be implemented.
    pass
