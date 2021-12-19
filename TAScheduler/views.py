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
        user = request.POST["name"]
        password = request.POST["password"]

        userobject = authenticate(request, username=user, password=password)

        if not (userobject == None):
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
        return render(request, "coursemanagement.html", {"Courses": courses, "Sections": sections, "Role":determineRole(request.user)})

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
            sections = list(Section.objects.filter(users__in = [ user ]) | Section.objects.filter(course__in = courses))
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
            if description == '':
                description = 'No description'
            
            course = Course(name = name, description = description)
            course.users.set([])

            course.save()

    def createSection(context):
        # TODO: group membership check.
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
        # To be implemented.
        pass

    def deleteSection(context):
        # To be implemented.
        pass

    def assignUser(context):
        # To be implemented.
        pass

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
            if (determineRole(i) == "manager"):
                Admin.append(i)
            elif (determineRole(i) == "instructor"):
                Instructor.append(i)
            elif (determineRole(i) == "ta"):
                TA.append(i)
        return render(request, "usermanagement.html",
                      {"TA": TA, "Instructor": Instructor, "Admin": Admin, "Profiles": Profiles,
                       "SideButtons": SideButtons, "UserButtons": UserButtons})

    def post(self, request):
        if all([(field in request.POST) and (request.POST[field] != '') for field in
                ['username', 'email', 'name', 'password']]):
            user = request.POST["username"]
            email = request.POST["email"]
            name = request.POST["name"]
            password = request.POST["password"]
            address = request.POST.get("address", "")
            phone = request.POST.get("phone", "")
            altemail = request.POST.get("altemail", "")
            usergroup = request.POST["groups"]

            form = {"username": user,
                    "email": email,
                    "name": name,
                    "password": password,
                    "address": address,
                    "phone": phone,
                    "altemail": altemail,
                    "groups": usergroup}
            self.determineForm(form)

        return redirect("/accountmanagement/")

    def determineForm(self, form):
        # if not createUser or deleteUser then ValueError
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
        user = User.objects.get(username=form["username"])
        user.delete()

    def load(self, currentUser):
        currentrole = determineRole(currentUser)
        # admin
        UserList = User.objects.all()
        print(UserList)

        if (currentrole == "manager"):
            ProfileList = Profile.objects.all()
            print("in manager")
            sidebutton = Button()
            sidebutton.value = "Create"
            userbutton = Button()
            userbutton.value = "Delete"

            SideButtons = [sidebutton]
            UserButtons = [userbutton]
        # instructor
        elif (currentrole == "instructor"):
            ProfileList = []
            SideButtons = []
            UserButtons = []
        # ta
        elif (currentrole == "ta"):
            ProfileList = []
            SideButtons = []
            UserButtons = []
        # determinerolebroke
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
        return load(request)

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
        role = determineRole(currentuser)
        if role == 'ta':
            self.TAProfile(currentprofile, request.POST["skills"])

        print("New address")
        print(currentprofile.address)
        return redirect("/profile/")

    def otherProfile(self, user, profile, post):
        newname=post["name"]
        newusername=post["username"]
        newemail=post["email"]
        if(newname!=""):
            currentuser.first_name = newname

            user.first_name=newname
        if(newusername!="" and len(User.objects.filter(username=newusername))==0):
            currentuser.username = newusername
            user.username=newusername
        if(newemail!=""):
            user.email=newemail
        user.save()

        newphone=post["phone"]
        newaddress=post["address"]
        newaltemail=post["altemail"]
        if(newphone!=""):
            currentprofile.phone = newphone
            profile.phone=newphone
        if(newaddress!=""):
            print("inside if statement")
            currentprofile.address = newaddress
        if (newemail != ""):
            currentuser.email = newemail
            profile.address=newaddress
        if (newaltemail!=""):
            currentprofile.alt_email = newaltemail
            profile.alt_email=newaltemail
        profile.save()
        pass

        currentuser.save()
        currentprofile.save()
        print("New address")
        print(currentprofile.address)
        return redirect("/profile/")
    def TAProfile(self, profile, skills):
        profile.skills = skills
        profile.save()
        pass
