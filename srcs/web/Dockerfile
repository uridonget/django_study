FROM python:3.6.5-slim

# 작업 디렉토리 설정
WORKDIR /app/src

COPY requirements.txt .

# 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN if [ ! -f "manage.py" ]; then django-admin startproject mysite .; fi

COPY init/mysite /app/src/mysite

# RUN python manage.py startapp polls
COPY init/polls /app/src/polls

RUN python manage.py makemigrations polls
RUN python manage.py migrate
RUN python manage.py shell < mysite/init_superuser.py

# 서버 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
