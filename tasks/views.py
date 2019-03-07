from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.text import slugify
from django.core.paginator import Paginator

from .utils import WelcomeView
from .models import Task, Tag
from .forms import LogingForm, CreateTaskForm, CreateTagForm, RegistrationForm


class Index(WelcomeView, View):
    def get(self, request):
        super().init()
        if request.user.is_authenticated:
            self.template = 'tasks/index.html'
            self.done = True if request.GET.get("done") else False
            tasks = Task.objects.filter(user=request.user).filter(
                parent=None).filter(done=self.done)
            paginator = Paginator(tasks, 6)
            page = request.GET.get('page')
            self.context['tasks'] = paginator.get_page(page)
        return render(request, self.template, self.context)


class TaskDetail(WelcomeView, View):
    def get(self, request, task_slug):
        super().init()
        if request.user.is_authenticated:
            self.template = 'tasks/detail.html'
            task = Task.objects.get(slug=task_slug)
            self.context['main_task'] = task
            self.context['edit_task_url'] = "/edit_task/" + task.slug
            self.context['tasks'] = task.children.all().order_by(
                'date_of_creation')[::-1]
        return render(request, self.template, self.context)


class TagIndex(WelcomeView, View):
    def get(self, request, tag_slug):
        super().init()
        if request.user.is_authenticated:
            self.template = 'tasks/tagIndex.html'
            task_tag = Tag.objects.get(slug=tag_slug)
            tasks = Task.objects.filter(user=request.user).filter(tag=task_tag)
            self.context['tasks'] = tasks
            self.context['tagName'] = task_tag.name
        return render(request, self.template, self.context)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class LoginUser(View):
    context = {'button': 'Вход'}
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


class Registration(View):
    context = {'button': 'Зарегистрироваться'}
    template = 'tasks/registration.html'

    def get(self, request):
        self.context['form'] = RegistrationForm()
        self.context['error'] = False
        return render(request, self.template, self.context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        self.context['form'] = form
        self.context['error'] = False
        if form.is_valid():
            self.checkValidForm(form)

            if not self.context['error']:
                user = self.registration(form)
                if user:
                    login(request, user)
                    return redirect("/")
        return render(request, self.template, self.context)

    def checkValidForm(self, form):
        if User.objects.filter(username=form.cleaned_data["username"]):
            self.context['error'] = True
            self.context['message'] = "Пользователь с таким именем уже существует."

        if form.cleaned_data["password"] != form.cleaned_data["checkPassword"]:
            self.context['error'] = True
            self.context['message'] = "Пароли не совпадают."

        if User.objects.filter(email=form.cleaned_data["email"]):
            self.context['error'] = True
            self.context['message'] = "Пользователь с такой почтой уже существует."

    def registration(self, form):
        user = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password"],
        )
        user.save()
        return user


class CreateTask(WelcomeView, View):
    def get(self, request, **kwargs):
        super().init()
        if request.user.is_authenticated:
            self.get_context(request)
            if kwargs.get('task_slug'):
                self.parent = Task.objects.get(slug=kwargs.get('task_slug'))
                self.context['parent'] = self.parent
        return render(request, self.template, self.context)

    def post(self, request, **kwargs):
        super().init()
        if request.user.is_authenticated:
            self.get_context(request, post=request.POST)
            if kwargs.get('task_slug'):
                self.parent = Task.objects.get(slug=kwargs.get('task_slug'))
                self.url = self.parent.get_absolute_url()
            if self.context['form'].is_valid():
                try:
                    self.create_task(request)
                    return redirect(self.url)
                except:
                    return render(request, self.template, self.context)
        return render(request, self.template, self.context)

    def get_context(self, request, post=None):
        self.template = 'tasks/createTask.html'
        self.context['form'] = CreateTaskForm(
        ) if post == None else CreateTaskForm(post)
        self.context['button'] = 'save'
        self.context['tags'] = Tag.objects.filter(user=request.user)
        self.parent = None
        self.url = '/'

    def create_task(self, request):
        self.task_title = self.context['form'].cleaned_data['title']
        self.task = Task(
            user=request.user,
            title=self.task_title,
            body=self.context['form'].cleaned_data['body'],
            slug=request.user.username + "_" + slugify(self.task_title)
        )
        if request.POST['task_tag'] != '---':
            self.task.tag = Tag.objects.get(id=int(request.POST['task_tag']))
        self.task.parent = self.parent
        self.task.save()


class EditTask(WelcomeView, View):
    def get(self, request, task_slug):
        super().init()
        if request.user.is_authenticated:
            self.get_context(request, task_slug)
        return render(request, self.template, self.context)

    def post(self, request, task_slug):
        super().init()
        if request.user.is_authenticated:
            self.get_context(request, task_slug, post=request.POST)
            if self.context['form'].is_valid():
                try:
                    self.create_task(request)
                    return redirect(self.url)
                except:
                    return render(request, self.template, self.context)
        return render(request, self.template, self.context)

    def get_context(self, request, task_slug, post=None):
        self.template = 'tasks/createTask.html'
        self.task = Task.objects.get(slug=task_slug)
        data = {'title': self.task.title, 'body': self.task.body}
        self.context['form'] = CreateTaskForm(
            data) if post == None else CreateTaskForm(post)
        self.context['button'] = 'save'
        self.context['tags'] = Tag.objects.filter(user=request.user)
        self.url = self.task.get_absolute_url()

    def create_task(self, request):
        self.task.title = self.context['form'].cleaned_data['title']
        self.task.body = self.context['form'].cleaned_data['body']
        if request.POST['task_tag'] != '---':
            self.task.tag = Tag.objects.get(id=int(request.POST['task_tag']))
        self.task.save()


class CreateTag(WelcomeView, View):
    def get(self, request):
        super().init()
        if request.user.is_authenticated:
            self.context['form'] = CreateTagForm()
            self.template = 'tasks/createTag.html'
        return render(request, self.template, self.context)

    def post(self, request):
        super().init()
        if request.user.is_authenticated:
            self.template = 'tasks/createTag.html'
            self.context['form'] = CreateTagForm(request.POST)
            if self.context['form'].is_valid():
                try:
                    self.name = self.context['form'].cleaned_data['name']
                    self.slug = request.user.username + \
                        "_" + slugify(self.name)
                    tag = Tag(
                        user=request.user,
                        name=self.name,
                        slug=self.slug
                    )
                    tag.save()
                    return redirect("/")
                except:
                    return render(request, self.template, self.context)
        return render(request, self.template, self.context)


class DoneTask(View):
    def get(self, request):
        return redirect("/")

    def post(self, request):
        task = Task.objects.get(slug=request.POST["slug"])
        done = True if request.POST["done"] == "true" else False
        for child in task.children.all():
            child.done = done
            child.save()
        task.done = done
        task.save()
        return HttpResponse("Ok", content_type="application/json")
