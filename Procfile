sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn vizva.wsgi:application --bind 0.0.0.0:$PORT"
