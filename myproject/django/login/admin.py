from django.contrib import admin
from .models import User

# 모델을 관리자 페이지에 등록
admin.site.register(User)