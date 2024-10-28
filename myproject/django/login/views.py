from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
import requests, json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'login/index.html')
