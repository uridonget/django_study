from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse, HttpResponse

def index(request):
    return render(request, 'lobby/index.html')