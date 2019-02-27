from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .utils.View import WelcomeView
from .models import Task, Tag
from .forms import LogingForm

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
    def get(self, request):
        form = LogingForm()
        return render(request, 'tasks/login.html', context={"form": form, "error": False})

    def post(self, request):
        bound_form = LogingForm(request.POST)
        if bound_form.is_valid():
            user = authenticate(request, username=bound_form.cleaned_data["username"], password=bound_form.cleaned_data["password"])       
            if user:
                login(request, user)
                return redirect("/")
        return render(request, 'tasks/login.html', context={"form": bound_form, "error": True})




