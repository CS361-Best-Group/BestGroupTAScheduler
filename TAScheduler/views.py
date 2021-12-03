from hashlib import sha256

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

class Login(View):

    def get(self, request):
        logout(request)
        print(Group.objects.all())
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
        return render(request, "coursemanagement.html")

    def post(self, request):
        pass


class AccountManagement(View):

    def get(self, request):


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