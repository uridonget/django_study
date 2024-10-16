#!/bin/sh

python manage.py makemigrations polls
python manage.py migrate
python manage.py shell < mysite/init_superuser.py

exec "$@"
