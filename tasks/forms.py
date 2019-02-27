from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LogingForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    username.widget.attrs.update({
        "class": "form-control",
        "type" : "text",
        "placeholder": "Enter username"
    })

    password.widget.attrs.update({
        "class": "form-control",
        "placeholder": "Enter password"
    })


class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body', 'tags', 'deadline']
