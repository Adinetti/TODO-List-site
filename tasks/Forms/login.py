from django import forms

class LogingForm(forms.Form):
    userName = forms.CharField(label='Your name', max_length=120)
    password = forms.PasswordInput(label='Password')