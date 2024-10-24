from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from .forms import GameLogForm
from .models import User,GameLog
from django.conf import settings
import requests

def index(request):
    return render(request, 'login/index.html')

def game_log(request):
    recent_games = GameLog.objects.order_by('-created_at')[:10]
    return render(request, 'login/game_log.html', {'recent_games': recent_games})

def create_game_log(request):
    if request.method == 'POST':
        form = GameLogForm(request.POST)
        if form.is_valid():
            user_a = form.cleaned_data['user_a']
            user_b = form.cleaned_data['user_b']
            user_a_score = form.cleaned_data['user_a_score']
            user_b_score = form.cleaned_data['user_b_score']

            # GameLog에 데이터 저장
            game_log = GameLog.objects.create(
                user_a=user_a,
                user_b=user_b,
                user_a_score=user_a_score,
                user_b_score=user_b_score
            )
            game_log.save()
            return redirect('game_log_success')  # 성공 후 이동할 페이지

    else:
        form = GameLogForm()

    return render(request, 'login/create_game_log.html', {'form': form})

def game_log_success(request):
    return render(request, 'login/game_log_success.html')

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
            return redirect('index')
        except User.DoesNotExist:
            # 유저가 존재하지 않는 경우, 회원가입 여부 확인 페이지로 이동
            return render(request, 'login/signup_confirm.html', {'user_info': user_info})
    else:
        return render(request, 'error.html', {'message': 'OAuth authentication failed.'})
    
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup_confirm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # 새로운 유저 생성
        user = User.objects.create(username=username, email=email)
        request.session['user_id'] = user.id

        return redirect('index')
    else:
        return render(request, 'error.html', {'message': 'Invalid request'})