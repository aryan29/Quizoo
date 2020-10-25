#!/bin/sh

set -e
service cron start
python3 manage.py collectstatic --noinput
python3 manage.py crontab add
uwsgi --socket :8000 --master --enable-threads --module quizoo.wsgi
