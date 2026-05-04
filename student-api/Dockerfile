# ---------- Base Image ----------
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_NO_DEV=1 \
    PATH="/app/.venv/bin:$PATH"

# ---------- Install uv (pinned) ----------
COPY --from=ghcr.io/astral-sh/uv:0.4.30 /uv /uvx /bin/

# ---------- Create non-root user ----------
RUN groupadd -g 999 appuser \
    && useradd -m -r -u 999 -g appuser appuser

# ---------- Set workdir ----------
WORKDIR /app

# ---------- Install system dependencies EARLY ----------
# (better caching; rarely changes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ---------- Copy dependency files ----------
COPY pyproject.toml uv.lock ./

# Install ONLY dependencies (no project yet)
RUN uv sync --locked --no-install-project

# ---------- Copy application code ----------
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY entrypoint.sh .

# Install the project itself
RUN uv sync --locked

# ---------- Fix permissions ----------
RUN chmod +x /app/entrypoint.sh \
    && chown -R appuser:appuser /app

# ---------- Switch to non-root ----------
USER appuser

# ---------- Run the application ----------
ENTRYPOINT ["/app/entrypoint.sh"]




