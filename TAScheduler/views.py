from django.shortcuts import render, redirect
from django.views import View

class Login(View):

    def get(self, request):
       return render(request, "login.html")

    def post(self):
        pass


class CourseCreation(View):

    def get(self, request):
        return render(request, "coursecreation.html")

    def post(self, request):
        pass


class AccountCreation(View):

    def get(self, request):
        return render(request, "accountcreation.html")

    def post(self, request):
        pass