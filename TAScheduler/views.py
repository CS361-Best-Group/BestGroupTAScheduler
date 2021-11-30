from django.shortcuts import render, redirect
from django.views import View


class Login(View):

    def get(self, request):
        request.session.clear()
        return render(request, "login.html")

    def post(self, request):
        pass



class CourseManagement(View):

    def get(self, request):
        return render(request, "courseManagement.html")

    def post(self, request):
        pass


class AccountManagement(View):

    def get(self, request):
        return render(request, "accountManagement.html")

    def post(self, request):
        pass

class Home(View):
    def get(self, request):
        return render(request, "home.html")

    def post(self, request):
        pass

class Profile(View):

    def get(self, request):
        return render(request, "profile.html")



    def post(self, request):
        pass