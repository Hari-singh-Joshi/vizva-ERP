FROM python:3.11-slim

# Prevent Python from writing .pyc files and force stdout/stderr flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run migrations + collectstatic at runtime with Railway’s env vars
CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn vizva.wsgi:application --bind 0.0.0.0:$PORT"
