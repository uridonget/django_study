from django.urls import path

from . import views

app_name = 'lobby'

urlpatterns = [
    path('', views.index, name='index'),
    path('game_log/', views.game_log, name='game_log'),
    path('create_game_log/', views.create_game_log, name='create_game_log'),
    path('game_log_success/', views.game_log_success, name='game_log_success'),
]