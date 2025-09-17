# Use official Python image
FROM python:3.12-slim

# Prevents Python from writing .pyc files and enables unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port from .env (default fallback if needed)
ARG DJANGO_PORT=8001
EXPOSE ${DJANGO_PORT}

# Run Gunicorn
CMD ["sh", "-c", "gunicorn vizva.wsgi:application --bind 0.0.0.0:${DJANGO_PORT} --workers 3"]
