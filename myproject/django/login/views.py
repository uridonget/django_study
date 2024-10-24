from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
import os
from .models import User
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # 세션에 user_id가 있는지 확인하여 로그인 여부를 판단
    if request.session.get('user_id'):
        # 로그인되어 있으면 'lobby:index'로 리디렉션
        return redirect(reverse('lobby:index'))
    else:
        # 로그인되지 않았으면 login 페이지 렌더링
        return render(request, 'login/index.html')

def login_oauth(request):
    client_id = os.environ.get('CLIENT_ID')
    redirect_uri = 'http://localhost:8000/oauth/callback/'
    state = 'random_string'
    authorize_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=public&state={state}"
    return redirect(authorize_url)

def oauth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    redirect_uri = 'http://localhost:8000/oauth/callback/'

    # 액세스 토큰 요청
    token_url = "https://api.intra.42.fr/oauth/token"
    response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    })
    if response.status_code == 200:
        access_token = response.json().get('access_token')

        # 액세스 토큰을 사용하여 유저 정보 가져오기
        user_info = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()

        try:
            user = User.objects.get(username=user_info['login'])
            # 유저가 이미 존재하는 경우, 로그인 처리
            request.session['user_id'] = user.id
            return redirect('lobby:index')
        except User.DoesNotExist:
            # 유저가 존재하지 않는 경우, 회원가입 여부 확인 페이지로 이동
            return render(request, 'login/signup_confirm.html', {'user_info': user_info})
    else:
        return render(request, 'error.html', {'message': 'OAuth authentication failed.'})

@csrf_exempt
def signup_confirm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # 유저 생성
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        
        # 세션 설정
        request.session['user_id'] = user.id

        # 원하는 URL로 리디렉트
        return redirect('lobby:index')
        # return render(request, 'lobby/index.html')
    else:
        # GET 요청의 경우 다른 처리
        return redirect('login:index')
        # return render(request, 'login/index.html')