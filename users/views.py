from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # Django's built-in User model
from django.contrib import messages  # For displaying messages like errors
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import UserProfile


def index(request):
    return HttpResponseRedirect(reverse('users:login'))


    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("products:index"))
        else:
            messages.error(request, "Invalid username and/or password.")
    return render(request, "users/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST.get("email")
        password = request.POST["password"]
        confirmation = request.POST.get("confirmation")
        college = request.POST.get("college")  # Capture college information
        if password == confirmation:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                user_profile = UserProfile.objects.get(user=user)
                user_profile.college = college
                user_profile.save()
                login(request, user)
                return HttpResponseRedirect(reverse("login"))
            except IntegrityError:
                messages.error(request, "Username already taken.")
        else:
            messages.error(request, "Passwords must match.")
    return render(request, "users/register.html")



    
