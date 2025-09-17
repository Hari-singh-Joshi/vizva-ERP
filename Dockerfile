FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ARG DJANGO_PORT=8001
EXPOSE ${DJANGO_PORT}

CMD ["sh", "-c", "python manage.py migrate && gunicorn vizva.wsgi:application --bind 0.0.0.0:${DJANGO_PORT} --workers 3"]
