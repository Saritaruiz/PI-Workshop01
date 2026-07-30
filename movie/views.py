from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name': 'Sara Ruizzz <3'})


def about(request):
    return render(request, 'about.html')
