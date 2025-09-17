FROM python:3.11-slim

# Prevent .pyc files and enable unbuffered output
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

# Collect static files (safe with Whitenoise)
RUN python manage.py collectstatic --noinput || true

# Start Gunicorn (Railway provides $PORT automatically)
CMD ["gunicorn", "vizva.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
