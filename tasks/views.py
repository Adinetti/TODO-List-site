from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.utils.text import slugify

from .utils import WelcomeView
from .models import Task, Tag
from .forms import LogingForm, CreateTaskForm


class Index(WelcomeView, View):
    def get(self, request):
        super().init()
        if request.user.is_authenticated:            
            self.template = 'tasks/index.html'
            self.done = False
            if(request.GET.get("done")):
                self.done = True
            tasks = Task.objects.filter(user=request.user).filter(
                parent=None).filter(done=self.done).order_by('date_of_creation')[::-1]
            self.context['tasks'] = tasks
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
        self.context['form'] = CreateTaskForm() if post == None else CreateTaskForm(post)
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
        data = {'title':self.task.title, 'body':self.task.body}
        self.context['form'] = CreateTaskForm(data) if post == None else CreateTaskForm(post)
        self.context['button'] = 'save'
        self.context['tags'] = Tag.objects.filter(user=request.user)       
        self.url = self.task.get_absolute_url()

    def create_task(self, request):
        self.task.title = self.context['form'].cleaned_data['title']
        self.task.body = self.context['form'].cleaned_data['body'] 
        if request.POST['task_tag'] != '---':   
            self.task.tag = Tag.objects.get(id=int(request.POST['task_tag']))
        self.task.save()


class DoneTask(View):
    def get(self, request):
        return redirect("/")

    def post(self, request):
        print(request.POST["slug"])
        task = Task.objects.get(slug=request.POST["slug"])
        for child in task.children.all():
            child.done = True
            child.save()
        task.done = True
        task.save()
        return HttpResponse("Ok", content_type="application/json")
