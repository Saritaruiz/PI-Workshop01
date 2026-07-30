from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name': 'Sara Ruiz'})


def about(request):
    return HttpResponse('<h1> Welcome to About Page Sara </h1>')
