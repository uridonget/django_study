# lobby/forms.py
from django import forms
from .models import User

class GameLogForm(forms.Form):
    user_a = forms.ModelChoiceField(queryset=User.objects.all(), label='User A')
    user_b = forms.ModelChoiceField(queryset=User.objects.all(), label='User B')
    user_a_score = forms.IntegerField(min_value=0, label='User A Score')
    user_b_score = forms.IntegerField(min_value=0, label='User B Score')