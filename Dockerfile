FROM python:3.11-slim

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

# Do NOT run collectstatic here (env vars not available yet)

# Run migrations + collectstatic at runtime
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn vizva.wsgi:application --bind 0.0.0.0:$PORT"]
