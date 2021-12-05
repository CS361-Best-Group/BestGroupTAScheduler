from hashlib import sha256

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User, Group



from TAScheduler.models import Course, Section

class Login(View):

    def get(self, request):
        logout(request)
        return render(request, "login.html")

    def post(self, request):
        user=request.POST["name"]
        password=request.POST["password"]



        userobject=authenticate(request, username=user, password=password)


        if not(userobject == None):
            login(request, userobject)
            return redirect("/")

        else:
            return render(request, "login.html")



class CourseManagement(View):

    def get(self, request):



        Courses=Course.objects.all()
        Sections=Section.objects.all()

        return render(request, "coursemanagement.html", {"Courses":Courses, "Sections":Sections})




    def post(self, request):



        if("coursename" in request.POST.keys() and "coursedescription" in request.POST.keys() and request.POST["coursename"] != "" and request.POST["coursedescription"] != ""):

            coursecreationName = request.POST["coursename"]

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


            newsection=Section(name=newsectionname)
            newsection.save()
            newsection.users.set([])
            newsection.course=targetcourse
            newsection.save()

        return redirect("/coursemanagement/")



    #how can I handle multiple forms on the same page?




class AccountManagement(View):

    def get(self, request):

        #Nothing will be mapped course fields if post is from a section creation form submission


        TA=User.objects.filter(groups__name='ta')
        Instructor=User.objects.filter(groups__name='instructor')
        Admin=User.objects.filter(groups__name='manager')



        return render(request, "usermanagement.html", {"TA":TA, "Instructor":Instructor, "Admin":Admin})


    def post(self, request):
        user=request.POST["username"]
        email=request.POST["email"]
        name=request.POST["name"]
        password=request.POST["password"]

        userthere=User.objects.filter(username=user)
        groups=Group.objects.filter(name="manager")
        groupthing=groups[0]

        if(len(userthere)==0):

            newuser=User.objects.create_user(username=user, email=email, first_name=name, password=password)

            newuser.groups.add(groupthing)
            newuser.save()


        return redirect("/accountmanagement/")




class Home(View):

    def get(self, request):
        return render(request, "index.html")


    def post(self, request):
        pass

class Profile(View):

    def get(self, request):
        return render(request, "profile.html")


    def post(self, request):
        pass