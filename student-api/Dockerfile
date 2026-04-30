# ---------- Base Image ----------
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ---------- Dependencies Layer ----------
FROM base AS deps

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN pip install --no-cache-dir uv \
    && uv pip install --system . \
    && rm -rf /root/.cache

# ---------- Final Runtime Image ----------
FROM base AS final

# Install runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

# Copy Python packages
COPY --from=deps /usr/local /usr/local

# Copy app files
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY entrypoint.sh .

# Set permissions
RUN chmod +x /app/entrypoint.sh \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]