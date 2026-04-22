# Declare commands (not files)
.PHONY: install run test migrate makemigration

# Install dependencies using uv
install:
	uv sync

# Run the FastAPI application
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests (fix import issue + ensure uv env is used)
test:
	PYTHONPATH=. uv run pytest