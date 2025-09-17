#!/bin/bash
set -o errexit  # exit if any command fails
set -o pipefail
set -o nounset

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
cd app && gunicorn vizva.wsgi:application --bind 0.0.0.0:$PORT

