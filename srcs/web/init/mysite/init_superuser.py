# init_superuser.py
from django.contrib.auth.models import User

username = 'admin'
email = 'admin@example.com'
password = 'password'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created.')
