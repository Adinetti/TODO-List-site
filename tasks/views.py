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
            tasks = Task.objects.filter(user=request.user).filter(parent=None)
            self.context['tasks'] = tasks
        return render(request, self.template, self.context)


class TaskDetail(WelcomeView, View):
    def get(self, request, task_slug):
        if request.user.is_authenticated:
            self.template = 'tasks/detail.html'
            task = Task.objects.get(slug=task_slug)
            self.context['main_task'] = task
            self.context['tasks'] = task.children.all()
        return render(request, self.template, self.context)


class Tag(WelcomeView, View):
    def get(self, request, tag_slug):
        if request.user.is_authenticated:
            self.template = 'tasks/index.html'
            task_tag = Tag.objects.get(slug=tag_slug)
            tasks = Task.objects.filter(
                user=request.user).filter(tags=task_tag)
            self.context['tasks'] = tasks
            self.context['tag'] = task_tag
        return render(request, self.template, self.context)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class LoginUser(View):
    context = {'button': 'Loging'}
    template = 'tasks/loging.html'

    def get(self, request):
        self.context['form'] = LogingForm()
        self.context['error'] = False
        return render(request, self.template, self.context)

    def post(self, request):
        self.context['form'] = LogingForm(request.POST)
        if self.context['form'].is_valid():
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
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            self.get_context()
        return render(request, self.template, self.context)

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            self.get_context(request.POST)
            if kwargs.get('task_slug'):
                self.parent = Task.objects.get(slug=kwargs.get('task_slug'))
                self.url = self.parent.get_absolute_url()
            if self.context['form'].is_valid():
                try:
                    self.create_task()
                    return redirect(self.url)
                except:
                    return render(request, self.template, self.context)
        return render(request, self.template, self.context)

    def get_context(self, post=None):
        self.template = 'tasks/createTask.html'
        self.context['form'] = CreateTaskForm() if post == None else CreateTaskForm(post)
        self.context['button'] = 'save'
        self.parent = None
        self.url = '/'

    def create_task():
        task_title = self.context['form'].cleaned_data['title']
        task = Task(
            user=request.user,
            title=task_title,
            body=self.context['form'].cleaned_data['body'],
            slug=request.user.username + "_" + slugify(task_title)
        )
        task.parent=self.parent
        task.save()
