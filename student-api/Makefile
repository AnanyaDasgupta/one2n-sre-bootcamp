# Declare commands (not files)
.PHONY: install run dev test lint format migrate makemigration upgrade downgrade current history reset-db

# Load environment variables if .env exists
ifneq (,$(wildcard .env))
include .env
export
endif

PORT ?= 8000

# ----------------------
# Install dependencies
# ----------------------
install:
	uv sync

# ----------------------
# Run app
# ----------------------
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

# Dev mode (auto reload)
dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

# ----------------------
# Testing & linting
# ----------------------
test:
	PYTHONPATH=. uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

# ----------------------
# Alembic (DB migrations)
# ----------------------

# Create migration (usage: make makemigration msg="your message")
makemigration:
	uv run alembic revision --autogenerate -m "$(msg)"

# Apply migrations
upgrade:
	uv run alembic upgrade head

# Rollback last migration
downgrade:
	uv run alembic downgrade -1

# Show current revision
current:
	uv run alembic current

# Show migration history
history:
	uv run alembic history --verbose

# Reset DB (⚠️ destructive, dev only)
reset-db:
ifndef ENV
	$(error ENV not set. Use ENV=dev)
endif
ifeq ($(ENV),prod)
	$(error Cannot reset production database)
endif
	uv run alembic downgrade base
	uv run alembic upgrade head