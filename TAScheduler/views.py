from hashlib import sha256

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User, Group
from TAScheduler.determinerole import determineRole

from TAScheduler.models import Course, Section

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



        Courses=Course.objects.all()
        Sections=Section.objects.all()

        return render(request, "coursemanagement.html", {"Courses":Courses, "Sections":Sections})



    def post(self, request):



        if("coursename" in request.POST.keys() and "coursedescription" in request.POST.keys() and request.POST["coursename"] != "" and request.POST["coursedescription"] != ""):

            coursecreationName = request.POST["coursename"]

            if(len(Course.objects.filter(name=coursecreationName))==0):
                coursecreationDescription = request.POST["coursedescription"]
                newcourse=Course(name=coursecreationName, description=coursecreationDescription)

                newcourse.save()
                newcourse.users.set([])
                newcourse.save()

        elif ("course" in request.POST.keys()):
            
            sectioncreationcourse = request.POST["course"]
            targetcourse=Course.objects.filter(name=sectioncreationcourse)[0]

            existingsections=str(len(Section.objects.filter(course=targetcourse))+1)
            newsectionname=targetcourse.name+"-"

            x=0
            while x+len(existingsections)<3:
                newsectionname=newsectionname+"0"
                x=x+1
            newsectionname=newsectionname+existingsections


            newsection=Section(name=newsectionname, course=targetcourse)
            newsection.save()
            newsection.users.set([])
#            newsection.course=targetcourse
            newsection.save()

        return redirect("/coursemanagement/")



    #how can I handle multiple forms on the same page?



class AccountManagement(LoginRequiredMixin, View):
    def get(self, request):
        # Nothing will be mapped course fields if post is from a section creation form submission

        TA = User.objects.filter(groups__name='ta')
        Instructor = User.objects.filter(groups__name='instructor')
        Admin = User.objects.filter(groups__name='manager')
        Profiles = Profile.objects.all()

        return render(request, "usermanagement.html",
                      {"TA": TA, "Instructor": Instructor, "Admin": Admin, "Profiles": Profiles})

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
            userthere = User.objects.filter(username=user)
            groups = Group.objects.filter(name="manager")
            groupthing = groups[0]

            if (len(userthere) == 0):
                newuser = User.objects.create_user(username=user, email=email, first_name=name, password=password)

                newuser.groups.add(groupthing)
                newuser.save()
                newProfile = Profile(user=newuser, address=address, phone=phone, alt_email=altemail)
                newProfile.save()

        return redirect("/accountmanagement/")

    def determineForm(self, form):
        # if not createUser or deleteUser then ValueError
        if ("username" not in form.keys()):
            print("Bad form given")
        # if all forms filled => createUser
        elif ("username" in form.keys() and "email" in form.keys() and "name" in form.keys() and "password" in form.keys()
                and "address" in form.keys() and "phone" in form.keys() and "altemail" in form.keys()
                and "groups" in form.keys()):
            AccountManagement.createUser(self, form)
        # if only username filled => deleteUser
        else:
            AccountManagement.deleteUser(self, form)

    def createUser(self, form):
        username = form["username"]
        if len(User.objects.all()) == 0:
            newuser = User.objects.create_user(username=form["username"], email=form["email"],
                                                first_name=form["name"], password=form["password"])
            newuser.save()
            newprofile = Profile(user=newuser, address=form["address"], phone=form["phone"],
                                 alt_email=form["altemail"])
            newprofile.save()
        elif len(User.objects.all()) != 0 and form["username"] in form.values():
            print("No duplicate users")
        else:
            newuser = User.objects.create_user(username=form["username"], email=form["email"],
                                                first_name=form["name"], password=form["password"])
            newuser.save()
            newprofile = Profile(user=newuser, address=form["address"], phone=form["phone"],
                                 alt_email=form["altemail"])
            newprofile.save()

    def deleteUser(self, form):
        user = User.objects.get(username=form["username"])
        user.delete()


class Home(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        pass

class ProfilePage(LoginRequiredMixin, View):
    def get(self, request):
        CurrentUserID=request.session["_auth_user_id"]
        CurrentUser=User.objects.filter(id=CurrentUserID)[0]
        CurrentProfile=Profile.objects.filter(user=CurrentUser)[0]

        return render(request, "profile.html", {"email":CurrentUser.email, "firstname":CurrentUser.first_name, "email":CurrentUser.email, "username":CurrentUser.username, "address":CurrentProfile.address, "phone":CurrentProfile.phone, "altemail":CurrentProfile.alt_email, "skills":CurrentProfile.skills})

    def post(self, request):
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
            user.first_name=newname
        if(newusername!="" and len(User.objects.filter(username=newusername))==0):
            user.username=newusername
        if(newemail!=""):
            user.email=newemail
        user.save()

        newphone=post["phone"]
        newaddress=post["address"]
        newaltemail=post["altemail"]
        if(newphone!=""):
            profile.phone=newphone
        if(newaddress!=""):
            print("inside if statement")
            profile.address=newaddress
        if (newaltemail!=""):
            profile.alt_email=newaltemail
        profile.save()
        pass

    def TAProfile(self, profile, skills):
        profile.skills = skills
        profile.save()
        pass

