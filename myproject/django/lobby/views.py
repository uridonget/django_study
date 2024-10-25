from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import GameLogForm
from .models import User, GameLog
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt

def authenticate_request(request):
    """
    JWT를 통해 요청을 인증하는 헬퍼 함수
    """
    auth_header = request.headers.get('Authorization')
    print("Authorization Header:", auth_header)  # Authorization 헤더 출력

    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 토큰에서 유저 ID 추출
            user = User.objects.get(id=user_id)
            print("User authenticated:", user)  # 유저 정보 출력
            return user
        except User.DoesNotExist:
            print("User does not exist for the provided user_id:", user_id)
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=401)
        except Exception as e:
            print("Token validation failed:", str(e))  # 에러 메시지 출력
            return JsonResponse({'status': 'error', 'message': 'Token validation failed'}, status=401)
    else:
        print("Authorization header missing or invalid")  # 헤더가 없는 경우 출력
        return JsonResponse({'status': 'error', 'message': 'Authorization header missing or invalid'}, status=401)

@csrf_exempt
def index(request):
    return render(request, 'lobby/index.html')

@csrf_exempt
def verify_token(request):
    """
    클라이언트 측에서 보내는 JWT를 검증하는 엔드포인트
    """
    return authenticate_request(request)

@csrf_exempt
def game_log(request):
    try:
        user = authenticate_request(request)  # JWT를 통해 유저 인증
        recent_games = GameLog.objects.order_by('-created_at')[:10]
        return render(request, 'lobby/game_log.html', {'recent_games': recent_games, 'user': user})
    except PermissionDenied:
        return redirect('login:index')

@csrf_exempt
def create_game_log(request):
    try:
        user = authenticate_request(request)  # JWT를 통해 유저 인증
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
                return redirect('lobby:game_log_success')  # 성공 후 이동할 페이지
        else:
            form = GameLogForm()

        return render(request, 'lobby/create_game_log.html', {'form': form, 'user': user})
    except PermissionDenied:
        return redirect('login:index')

@csrf_exempt
def game_log_success(request):
    try:
        user = authenticate_request(request)  # JWT를 통해 유저 인증
        return render(request, 'lobby/game_log_success.html', {'user': user})
    except PermissionDenied:
        return redirect('login:index')