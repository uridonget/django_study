from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # 세션이 아닌 JWT로 로그인 여부를 판단해야 하므로,
    # 클라이언트 측에서 JWT를 검증하는 로직을 작성하거나,
    # 프론트엔드에서 로그인 상태를 유지하는 방식으로 변경 필요
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
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        access_token = response.json().get('access_token')

        # 액세스 토큰을 사용하여 유저 정보 가져오기
        user_info = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()

        try:
            user = User.objects.get(username=user_info['login'])
            # 유저가 이미 존재하는 경우, JWT 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            print("access_token: ", access_token)
            print("refresh_token: ", refresh_token)

            # 로그인 성공 후 JWT를 URL 파라미터로 전달하여 클라이언트가 세션 스토리지에 저장할 수 있도록 함
            response = redirect(reverse('login:index'))
            response['Location'] += f'?access={access_token}&refresh={refresh_token}'
            return response

        except User.DoesNotExist:
            print("User not exist in Database")
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
        
        # 유저 생성 후 JWT 발급
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        print("User Created!")
        print("Access Token: ", access_token)
        # 회원가입 성공 후 JWT를 URL 파라미터로 전달하여 클라이언트가 세션 스토리지에 저장할 수 있도록 함
        response = redirect(reverse('login:index'))
        response['Location'] += f'?access={access_token}&refresh={refresh_token}'
        return response
    else:
        # GET 요청의 경우 다른 처리
        return redirect('login:index')
