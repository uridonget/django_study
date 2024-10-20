FROM python:3.11.4-slim

WORKDIR /app/django

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +x /app/django/entrypoint.sh

ENTRYPOINT ["/app/django/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
