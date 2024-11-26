from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10)  # 사용자 이름
    email = models.EmailField(max_length=50)    # 이메일
    win = models.IntegerField(default=0)        # 승리 횟수
    lose = models.IntegerField(default=0)       # 패배 횟수
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return self.username
