#!/bin/sh
set -e

until pg_isready -d "$DATABASE_URL"; do
  sleep 2
done

alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8000