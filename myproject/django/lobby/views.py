from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from .forms import GameLogForm
from .models import User,GameLog
from django.conf import settings
import requests

def index(request):
    return render(request, 'lobby/index.html')

def game_log(request):
    recent_games = GameLog.objects.order_by('-created_at')[:10]
    return render(request, 'lobby/game_log.html', {'recent_games': recent_games})

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

    return render(request, 'lobby/create_game_log.html', {'form': form})

def game_log_success(request):
    return render(request, 'lobby/game_log_success.html')
