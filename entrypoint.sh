#!/usr/bin/env bash
set -e

# Optional: show where we are
echo "Running entrypoint in $(pwd)"

# Apply database migrations
uv run python manage.py makemigrations --noinput
uv run python manage.py migrate --noinput

# If you also want to collect static files for templates:
# python manage.py collectstatic --noinput

# Finally run whatever command Docker passes (e.g. runserver or gunicorn)
exec "$@"
