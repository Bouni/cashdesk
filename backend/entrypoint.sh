#!/bin/sh

python3 /app/manage.py makemigrations --noinput
python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput 

ls -la /app

exec gunicorn --bind :8000 --workers 3 cashdesk.wsgi
