from django import forms
from .models import Task, Tag
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class LogingForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    username.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Введите свой логин'
    })

    password.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Введите свой пароль'
    })


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    checkPassword = forms.CharField(
        label="Проверка пароля", widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)

    username.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Введите свой логин'
    })

    password.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Введите свой пароль'
    })

    checkPassword.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Введите свой пароль еще раз'
    })

    email.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Введите свой email'
    })


class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название тэга'
            })
        }


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя задания'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание задания'
            })
        }
