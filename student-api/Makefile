.PHONY: run dev test lint

# Run the app (production-like)
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run in dev mode (auto-reload)
dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	uv run pytest -v

# Optional: lint
lint:
	uv run ruff check .