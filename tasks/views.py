from django.shortcuts import render

def wellcome(request):
    return render(request, 'tasks/base.html')
