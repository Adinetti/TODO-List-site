from django import forms
from .models import Task, Tag
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LogingForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    username.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Enter username'
    })

    password.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Enter password'
    })


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe task'
            })
        }

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        #self.fields['tag'].queryset = Tag.objects.filter(user_id=self.instance.user)
