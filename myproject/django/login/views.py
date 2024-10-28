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

def login_oauth(request):
    client_id = os.environ.get('CLIENT_ID')
    redirect_uri = 'http://localhost:8000/oauth/callback/'
    authorize_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=public"
    return redirect(authorize_url)

def oauth_callback(request):
    code = request.GET.get('code')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    redirect_uri = 'http://localhost:8000/oauth/callback/'

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
        
        user_info = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()

        try:
            user = User.objects.get(username=user_info['login'])

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # 로그인 성공 후 JWT를 URL 파라미터로 전달하여 클라이언트가 세션 스토리지에 저장할 수 있도록 함
            response = redirect(reverse('login:login_success'))
            response['Location'] += f'?access={access_token}&refresh={refresh_token}'
            return response
        except User.DoesNotExist: # 유저가 존재하지 않는 경우, 회원가입 여부 확인 페이지로 이동
            return render(request, 'login/signup_confirm.html', {'user_info': user_info})
    else:
        return render(request, 'error.html', {'message': 'OAuth authentication failed.'})

@csrf_exempt
def signup_confirm(request):
    if request.method == 'POST':
        # OK 버튼을 누르면 토큰 발급 후 유저 등록
        username = request.POST.get('username')
        email = request.POST.get('email')

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = redirect(reverse('login:login_success'))
        response['Location'] += f'?access={access_token}&refresh={refresh_token}'
        return response
    else:
        # NO 버튼을 누르면 초기 페이지로 다시 이동
        return redirect('login:index')

@csrf_exempt  # CSRF 토큰 검증을 비활성화 (AJAX 요청 시 필요)
def validate_token(request):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        print("Authorization Header:", auth_header)  # 콘솔에 auth_header 내용 출력
        
        # Authorization 헤더가 존재하고, "Bearer "로 시작하는지 확인
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]  # "Bearer " 이후의 토큰 추출
            try:
                # AccessToken을 사용하여 토큰 검증
                access_token = AccessToken(token)

                # 토큰이 유효하면 토큰에 포함된 사용자 정보나 추가 데이터를 사용 가능
                user_id = access_token['user_id']  # 예시로 user_id 추출
                user = User.objects.get(id=user_id)
                
                return JsonResponse({'valid': True, 'user_id': user_id, 'username': user.username})
            except AuthenticationFailed as e:
                # 토큰이 유효하지 않을 때의 처리 (예: 만료되었거나 잘못된 토큰)
                return JsonResponse({'valid': False, 'error': str(e)}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'valid': False, 'error': 'User does not exist.'}, status=401)
        
        # Authorization 헤더가 없거나 잘못된 경우
        return JsonResponse({'valid': False, 'error': 'Authorization header missing or invalid.'}, status=401)
    else:
        # POST 이외의 메서드로 접근했을 경우
        return JsonResponse({'valid': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def login_success(request):
    return render(request, 'login/login_success.html')

