# Build stage
FROM python:3.14-slim AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install --system .

# Runtime stage
FROM python:3.14-slim

WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]