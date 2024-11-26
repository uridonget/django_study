from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

# serve를 사용하여 static/index.html을 직접 반환합니다.
# STATICFILES_DIRS[0]은 myproject/static 디렉토리를 가리킵니다.

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^.*$', serve, {'path': 'index.html', 'document_root': settings.STATICFILES_DIRS[0]}),
]
