#!/bin/bash
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --workers 2 --threads 4 --bind 0.0.0.0:$PORT
