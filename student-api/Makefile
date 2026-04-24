# Declare commands (not files)
.PHONY: install run dev test lint migrate makemigration

ifneq (,$(wildcard .env))
include .env
export
endif

PORT ?= 8000

# Install dependencies using uv
install:
	uv sync

# Run the app (production-like)
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

# Run in dev mode (auto-reload)
dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

# Run tests
test:
	PYTHONPATH=. uv run pytest

# Optional: lint
lint:
	uv run ruff check .