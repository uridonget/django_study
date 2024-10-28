from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('', views.index, name='index'),
    path('login_oauth/', views.login_oauth, name='login_oauth'),
    path('oauth/callback/', views.oauth_callback, name='oauth_callback'),
    path('signup_confirm/', views.signup_confirm, name='signup_confirm'),
    path('success/', views.login_success, name='login_success'),
]