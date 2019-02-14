from django.shortcuts import render
from django.http import HttpResponse

def wellcome(request):
    return HttpResponse("Hello, World!")
