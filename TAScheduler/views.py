import time
from hashlib import sha256

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User, Group
from TAScheduler.determinerole import determineRole
from django.db.utils import IntegrityError

from TAScheduler.models import Course, Section

from .button import Button


class Login(View):

    def get(self, request):
        logout(request)
        return render(request, "login.html")

    def post(self, request):
        print("In post")
        user=request.POST["name"]
        password=request.POST["password"]

        userobject=authenticate(request, username=user, password=password)

        if not(userobject == None):
            print("Login")
            login(request, userobject)
            return redirect("/")

        else:
            return render(request, "login.html")


class CourseManagement(LoginRequiredMixin, View):
    def get(self, request):
        courses, sections = CourseManagement.load(request.user)
        print(courses)
        print(sections)
        print(request.user.groups.all()[0].name)
        instructors = []
        users = User.objects.all()
        for i in users:
            if determineRole(i) == "instructor" or determineRole(i)=="ta":
                instructors.append(i)
        return render(request, "coursemanagement.html", {"Courses": courses, "Sections": sections, "Role":determineRole(request.user), "instructors":instructors})

    def post(self, request):
        CourseManagement.handleForm(request.POST)
        return redirect("/coursemanagement/")

    # Data filtering and display functions.

    def getAssociatedInstructors(course):
        # To be implemented.
        pass

    def getAssociatedTAs(course):
        # To be implemented.
        pass

    def load(user):
        role = determineRole(user)

        if role == 'manager':
            courses = list(Course.objects.all())
            sections = list(Section.objects.all())
        elif role == 'instructor':
            courses = list(Course.objects.filter(users__in = [ user ]))
            sections = list(Section.objects.filter(course__in = courses))
        else:
            courses = list(Course.objects.filter(users__in = [ user ]))
            sections = list(Section.objects.filter(users__in = [ user ]))

            for section in sections:
                if section.course not in courses:
                    courses.append(section.course)

        return (courses, sections)
            
    # Form handling functions.

    def handleForm(context):
        formHandlers = {
            'createCourse': CourseManagement.createCourse,
            'createSection': CourseManagement.createSection,
            'deleteCourse': CourseManagement.deleteCourse,
            'deleteSection': CourseManagement.deleteSection,
            'assignUser': CourseManagement.assignUser
        }

        if 'kind' in context.keys():
            formHandlers.get(context['kind'], lambda *args, **keyArgs: None)(context)

    def createCourse(context):
        name = context.get('course', '')

        if name != '' and len(Course.objects.filter(name = name)) == 0:
            description = context.get('description', 'No description')
            if description == '':
                description = 'No description'

            course = Course(name = name, description = description)
            course.users.set([])

            course.save()

    def createSection(context):
        try:
            course = Course.objects.get(name = context.get('course', ''))
            name = context.get('section', '')

            if name != '' and len(Section.objects.filter(course = course, name = name)) == 0:
                section = Section(name = name, course = course)
                section.users.set([])
                section.save()
        except Course.DoesNotExist:
            pass

    def deleteCourse(context):
        try:
            course = Course.objects.get(name = context.get('course', ''))
            course.delete()
        except Course.DoesNotExist:
            pass

    def deleteSection(context):
        try:
            course = Course.objects.get(name = context.get('course', ''))
            section = Section.objects.get(course = course, name = context.get('section', ''))
            section.delete()
        except Course.DoesNotExist:
            pass
        except Section.DoesNotExist:
            pass

    def assignUser(context):
        # To be implemented.
        #assign to section
        if("section" in context.keys()):
            targetsection=Section.objects.filter(name=context["section"])[0]
            targetuser=User.objects.filter(first_name=context["user"])[0]
            targetsection.users.add(targetuser)
            print(len(Section.objects.all()))
            print(targetsection.users)
            print(len(Section.objects.all()))
        elif ("course" in context.keys()):
            targetcourse=Course.objects.filter(name=context["course"])[0]
            print(context.keys())
            targetuser = User.objects.filter(first_name=context["user"])[0]

            targetcourse.users.add(targetuser)
            print(targetcourse.users)
class AccountManagement(LoginRequiredMixin, View):
    def get(self, request):


        currentuserid=request.session["_auth_user_id"]
        currentUser=User.objects.filter(id=currentuserid)[0]
        Largelist=self.load(currentUser)
        Profiles=Largelist[1]
        SideButtons=Largelist[2]
        UserButtons=Largelist[3]

        TA=[]
        Instructor=[]
        Admin=[]

        for i in Largelist[0]:
            if(determineRole(i)=="manager"):
                Admin.append(i)
            elif (determineRole(i)=="instructor"):
                Instructor.append(i)
            elif (determineRole(i)=="ta"):
                TA.append(i)
        return render(request, "usermanagement.html",
                      {"TA": TA, "Instructor": Instructor, "Admin": Admin, "Profiles": Profiles,
                       "SideButtons": SideButtons, "UserButtons": UserButtons})

    def post(self, request):


        form=request.POST

        self.determineForm(form)

        return redirect("/accountmanagement/")

    def determineForm(self, form):
        # if not createUser or deleteUser then ValueError
        print("In determineForm")
        if "username" not in form.keys():
            print("Bad form given")
        # if all forms filled => createUser
        elif (
                "username" in form.keys() and "email" in form.keys() and "name" in form.keys() and "password" in form.keys()
                and "address" in form.keys() and "phone" in form.keys() and "altemail" in form.keys()
                and "groups" in form.keys()):
            AccountManagement.createUser(self, form)
        # if only username filled => deleteUser
        else:
            AccountManagement.deleteUser(self, form)

    def createUser(self, form):
        try:
            newuser = User.objects.create_user(username=form["username"], email=form["email"],
                                                first_name=form["name"], password=form["password"])

            group = Group.objects.get_or_create(name=form["groups"])
            newuser.groups.add(group[0])

            newuser.save()
            newprofile = Profile(user=newuser, address=form["address"], phone=form["phone"],
                                 alt_email=form["altemail"])
            newprofile.save()
        except IntegrityError:
            return redirect("/accountmanagement/")

    def deleteUser(self, form):
        print("Made it into form")
        user = User.objects.get(username=form["username"])
        print(user)
        user.delete()

    def load(self, currentUser):
        currentrole=determineRole(currentUser)
        #admin
        UserList = User.objects.all()
        print(UserList)

        if(currentrole=="manager"):
            ProfileList=Profile.objects.all()
            print("in manager")
            sidebutton=Button()
            sidebutton.value="Create"
            userbutton=Button()
            userbutton.value="Delete"

            SideButtons=[sidebutton]
            UserButtons=[userbutton]
        #instructor
        elif(currentrole=="instructor"):
            ProfileList=[]
            SideButtons=[]
            UserButtons=[]
        #ta
        elif(currentrole=="ta"):
            ProfileList=[]
            SideButtons=[]
            UserButtons=[]
        #determinerolebroke
        else:
            pass

        return [UserList, ProfileList, SideButtons, UserButtons]


class Home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        pass


class ProfilePage(LoginRequiredMixin, View):
    def get(self, request):
        return ProfilePage.load(self, request)

    def load(self, request):
        CurrentUserID=request.session["_auth_user_id"]
        CurrentUser=User.objects.filter(id=CurrentUserID)[0]

        CurrentProfile=Profile.objects.filter(user=CurrentUser)[0]

        if determineRole(CurrentUser) == 'ta':
            return render(request, "profile.html",
                          {"email":CurrentUser.email,
                           "firstname":CurrentUser.first_name,
                           "email":CurrentUser.email,
                           "username":CurrentUser.username,
                           "address":CurrentProfile.address,
                           "phone":CurrentProfile.phone,
                           "altemail":CurrentProfile.alt_email,
                           "skills":CurrentProfile.skills})
        else:
            return render(request, "profile.html",
                          {"email":CurrentUser.email,
                           "firstname":CurrentUser.first_name,
                           "email":CurrentUser.email,
                           "username":CurrentUser.username,
                           "address":CurrentProfile.address,
                           "phone":CurrentProfile.phone,
                           "altemail":CurrentProfile.alt_email}) #just don't return skills

    def post(self, request):
        newname = request.POST["name"]
        newusername = request.POST["username"]
        newphone = request.POST["phone"]
        newaddress = request.POST["address"]
        newemail = request.POST["email"]
        newaltemail = request.POST["altemail"]

        currentuser=User.objects.filter(id=request.session["_auth_user_id"])[0]
        currentprofile=Profile.objects.filter(user=currentuser)[0]

        self.otherProfile(currentuser, currentprofile, request.POST)
        if(determineRole(currentuser) == 'ta'):
            self.TAProfile(currentprofile, request.POST["skills"])

        print("Post username = " + currentuser.username)
        print("Post skills = " + currentprofile.skills)

        return redirect("/profile/")

    def otherProfile(self, user, profile, post):
        newname=post["name"]
        newusername=post["username"]
        newemail=post["email"]
        if(newname!=""):
            user.first_name = newname

            user.first_name=newname
        if(newusername!="" and len(User.objects.filter(username=newusername))==0):
            user.username = newusername
            user.username=newusername
        if(newemail!=""):
            user.email=newemail
        user.save()

        newphone=post["phone"]
        newaddress=post["address"]
        newaltemail=post["altemail"]
        if(newphone!=""):
            profile.phone = newphone
            profile.phone=newphone
        if(newaddress!=""):
            profile.address = newaddress
        if (newemail != ""):
            user.email = newemail
            profile.address=newaddress
        if (newaltemail!=""):
            profile.alt_email = newaltemail
            profile.alt_email=newaltemail

        profile.save()

        user.save()
        profile.save()
        print("New address")
        print(profile.address)
        return redirect("/profile/")
    def TAProfile(self, profile, skills):
        profile.skills = skills
        profile.save()
