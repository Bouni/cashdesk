#!/usr/bin/bash

killall -q screen

cd backend && screen -d -m -S cashdesk-backend ./manage.py runserver 0.0.0.0:9999

cd ..

cd frontend && screen -d -m -S cashdesk-frontend yarn run serve

