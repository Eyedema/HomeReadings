# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build

# Configure uv to manage a venv at /venv
ENV UV_PROJECT_ENVIRONMENT=/venv \
    UV_NO_MANAGED_PYTHON=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Get the uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install system deps only if you need them (build tools, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Create venv + install deps into /venv
RUN uv sync --no-editable

# Now copy the rest of the project
COPY . .

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directory for SQLite file (will be a volume)
RUN mkdir -p /data

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uv", "run", "gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--forwarded-allow-ips=*"]