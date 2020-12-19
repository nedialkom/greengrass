#!/bin/sh

source /var/app/venv/staging-LQM1lest/bin/activate
python /var/app/current/manage.py migrate
python /var/app/current/manage.py createsu
python /var/app/current/manage.py collectstatic --noinput