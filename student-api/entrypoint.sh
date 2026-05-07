#!/bin/sh

set -e

export PATH="/app/.venv/bin:$PATH"

wait_for_database() {
  echo "Waiting for database..."

  until pg_isready -d "$DATABASE_URL"; do
    sleep 2
  done

  echo "Database is ready!"
}

run_migrations() {
  current_revision="$(alembic current 2>/dev/null | awk '{print $1}')"
  head_revision="$(alembic heads | awk '{print $1}')"

  if [ -n "$current_revision" ] && [ "$current_revision" = "$head_revision" ]; then
    echo "Migrations already applied ($current_revision)."
    return
  fi

  echo "Running migrations..."
  alembic upgrade head
}

case "$1" in
  migrate)
    wait_for_database
    run_migrations
    ;;
  start | "")
    wait_for_database
    run_migrations
    echo "Starting app..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;
  *)
    exec "$@"
    ;;
esac
