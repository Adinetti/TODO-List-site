from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Task, Tag

def index(request):
    template = 'tasks/wellcome.html'
    context = {}
    if request.user.is_authenticated:
        template = 'tasks/index.html'
        tasks = Task.objects.filter(user=request.user)
        context['tasks'] = tasks
    return render(request, template, context)

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

def tag(request, tag_slug):
    template = 'tasks/wellcome.html'
    context = {}
    if request.user.is_authenticated:
        task_tag = Tag.objects.get(slug=tag_slug)
        template = 'tasks/index.html'
        tasks = Task.objects.filter(user=request.user).filter(tags=task_tag)
        context['tasks'] = tasks
        context['tag'] = task_tag
    return render(request, template, context)

