from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.utils.text import slugify

from .utils import WelcomeView
from .models import Task, Tag
from .forms import LogingForm, CreateTaskForm

class Index(WelcomeView, View):
    def get(self, request):        
        if request.user.is_authenticated:
            self.template = 'tasks/index.html'
            tasks = Task.objects.filter(user=request.user)
            self.context['tasks'] = tasks
        return render(request, self.template, self.context)


class Tag(WelcomeView, View):
    def get(self, request, tag_slug):
        if request.user.is_authenticated:
            self.template = 'tasks/index.html'
            task_tag = Tag.objects.get(slug=tag_slug)            
            tasks = Task.objects.filter(user=request.user).filter(tags=task_tag)
            self.context['tasks'] = tasks
            self.context['tag'] = task_tag
        return render(request, self.template, self.context)

class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect("/")

class LoginUser(View):
    context = {}    

    def get(self, request):
        if request.user.is_authenticated:
            self.template = 'tasks/login.html'
            self.context['form'] = LogingForm()
            self.context['error'] = False
        return render(request, self.template, self.context)

    def post(self, request):
        if request.user.is_authenticated:
            self.template = 'tasks/login.html'
            self.context['form'] = LogingForm(request.POST)
            if bound_form.is_valid():
                user = authenticate(
                    request, 
                    username=self.context['form'].cleaned_data["username"], 
                    password=self.context['form'].cleaned_data["password"]
                )       
                if user:
                    login(request, user)
                    return redirect("/")
        return render(request, self.template, self.context)


class CreateTask(WelcomeView, View):
    def get(self, request):
        if request.user.is_authenticated:
            self.template = 'tasks/createTask.html'
            form = CreateTaskForm()
            self.context['form'] = form
            self.context['button'] = 'save'
        return render(request, self.template, self.context)

    def post(self, request):
        if request.user.is_authenticated:
            self.template = 'tasks/createTask.html'
            bound_form = CreateTaskForm(request.POST)
            self.context['form'] = bound_form
            self.context['button'] = 'save'
            if bound_form.is_valid():
                try:
                    task_title = bound_form.cleaned_data['title']
                    task = Task(
                        user = request.user,
                        title = task_title,
                        body = bound_form.cleaned_data['body'],
                        slug = request.user.username + "_" + slugify(task_title)
                    )
                    task.save()
                    return redirect('/')
                except:
                    return render(request, self.template, self.context)
        return render(request, self.template, self.context)

