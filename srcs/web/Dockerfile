FROM python:3.11.4-slim

# 작업 디렉토리 설정
WORKDIR /app/src

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN if [ ! -f "manage.py" ]; then django-admin startproject mysite .; fi

COPY init/mysite /app/src/mysite
COPY init/polls /app/src/polls

RUN curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

RUN chmod +x mysite/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/wait-for-it.sh", "db:5432", "--"]
CMD ["mysite/entrypoint.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
