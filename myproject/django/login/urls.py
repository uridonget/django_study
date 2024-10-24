from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game_log/', views.game_log, name='game_log'),
    path('create-game-log/', views.create_game_log, name='create_game_log'),
    path('game-log-success/', views.game_log_success, name='game_log_success'),

    path('login_oauth/', views.login_oauth, name='login_oauth'),
    path('oauth/callback/', views.oauth_callback, name='oauth_callback'),
    path('signup_confirm/', views.signup_confirm, name='signup_confirm'),
]