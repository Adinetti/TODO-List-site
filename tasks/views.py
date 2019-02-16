from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def wellcome(request):
    if request.user.is_authenticated:
        return redirect("/{}".format(request.user.username))
    return render(request, 'tasks/wellcome.html')

def index(request, username):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request, 'tasks/index.html')

def logout_user(request):
    logout(request)
    return redirect("/")

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/{}".format(username))
    return render(request, 'tasks/login.html')