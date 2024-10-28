from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse, HttpResponse
from .models import User

def authenticate_request(request):
    """
    JWT를 통해 요청을 인증하는 헬퍼 함수 - Authorization 헤더에서 토큰 추출
    """
    # Authorization 헤더에서 토큰 추출
    auth_header = request.headers.get('Authorization')
    print("Authorization Header:", auth_header)  # Authorization 헤더 내용 출력

    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]  # "Bearer " 이후의 토큰 추출
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 토큰에서 유저 ID 추출
            user = User.objects.get(id=user_id)
            print("User authenticated:", user)  # 유저 정보 출력
            return user
        except User.DoesNotExist:
            print("User does not exist for the provided user_id:", user_id)
            raise PermissionDenied('User does not exist')
        except Exception as e:
            print("Token validation failed:", str(e))  # 토큰 검증 실패 메시지 출력
            raise PermissionDenied('Invalid or expired token')
    else:
        # Authorization 헤더가 없거나 잘못된 경우
        print("Authorization header missing or invalid")
        raise PermissionDenied('Authorization header missing or invalid')

@csrf_exempt
def index(request):
    # JWT 인증을 먼저 수행
    print(request)
    user = authenticate_request(request)
    if user is None:
        return redirect('login:index')

    print("USER DICT: ", user.__dict__)
    return render(request, 'lobby/index.html', {'user': user})