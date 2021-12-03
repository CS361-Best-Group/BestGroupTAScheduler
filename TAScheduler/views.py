from hashlib import sha256

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout


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
        return render(request, "coursemanagement.html")

    def post(self, request):
        pass


class AccountManagement(View):

    def get(self, request):
        return render(request, "usermanagement.html")

    def post(self, request):
        pass


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