from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10)  # 사용자 이름
    email = models.EmailField(max_length=50)    # 이메일
    win = models.IntegerField(default=0)        # 승리 횟수
    lose = models.IntegerField(default=0)       # 패배 횟수
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return self.username
    
class GameLog(models.Model):
    user_a = models.ForeignKey(User, related_name='games_as_user_a', null=True, on_delete=models.SET_NULL)  # 사용자 A (Foreign Key)
    user_b = models.ForeignKey(User, related_name='games_as_user_b', null=True, on_delete=models.SET_NULL)  # 사용자 B (Foreign Key)
    user_a_score = models.IntegerField(default=0)  # 사용자 A 점수
    user_b_score = models.IntegerField(default=0)  # 사용자 B 점수
    created_at = models.DateTimeField(auto_now_add=True)  # 게임 생성 시간

    def __str__(self):
        return f"{self.user_a} {self.user_b}"

