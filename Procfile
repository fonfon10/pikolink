release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn config.wsgi:application --workers 2 --threads 4 --bind 0.0.0.0:$PORT
