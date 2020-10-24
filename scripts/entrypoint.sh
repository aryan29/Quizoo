#!/bin/sh

set -e
python manage.py collectstatic --noinput
python manage.py crontab add
uwsgi --socket :8000 --master --enable-threads --module quizoo.wsgi
