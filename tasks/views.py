from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def index(request):
    template = 'tasks/wellcome.html'
    if request.user.is_authenticated:
        template = 'tasks/index.html'
    return render(request, template)

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
            return redirect("/")
    return render(request, 'tasks/login.html')