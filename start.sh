set -e

export DATABASE_URL="${DATABASE_URL}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec gunicorn vizva.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
