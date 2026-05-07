#!/bin/sh

export PATH="/app/.venv/bin:$PATH"

echo "Waiting for database..."

until pg_isready -d "$DATABASE_URL"; do
  sleep 2
done

echo "Database is ready!"

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec fastapi run app/main.py --port 8000 --host 0.0.0.0