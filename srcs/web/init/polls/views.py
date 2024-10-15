from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "polls/index.html")

def detail(request):
    return render(request, "polls/detail.html")
