#!/bin/sh

python3 /app/manage.py makemigrations --noinput
python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput 

exec supervisord -c /etc/supervisor/supervisord.conf
