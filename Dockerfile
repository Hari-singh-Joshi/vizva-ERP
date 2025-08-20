# ---------- Builder: install build deps & Python wheels ----------
FROM python:3.12.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for building common Python packages (psycopg, Pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps into a virtualenv so we can copy it to the runtime image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Use Docker layer caching: copy only requirements first
COPY requirements.txt ./
RUN pip install -r requirements.txt

# ---------- Runtime: minimal deps, non-root, copy venv & app ----------
FROM python:3.12.10-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install only runtime OS libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    zlib1g \
    libmagic1 \
    netcat-openbsd \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 10001 appuser

# Copy the virtualenv from the builder
COPY --from=builder /opt/venv /opt/venv

# Copy project files
COPY . /app

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Make directories for static/media (bind mounts or named volumes recommended)
RUN mkdir -p /app/staticfiles /app/media && chown -R appuser:appuser /app

USER appuser

# Optional healthcheck (hits your app's health endpoint)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8000/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "vizva.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "3", "-k", "gthread", "--threads", "4", "--timeout", "60"]
