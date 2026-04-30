# Student API

A simple FastAPI service for managing student records.
This project demonstrates a clean backend structure with routes, services, schemas, models, and database migrations.

---

## Features

* CRUD operations for students
* Versioned APIs (`/api/v1`)
* Health check endpoint
* SQLAlchemy for database access
* Alembic for schema migrations
* Environment-based configuration
* Integration tests with isolated PostgreSQL instances

---

## Project Structure

```text
student-api/
├── alembic/                # Migration configuration and versions
├── app/
│   ├── api/v1/            # Route handlers
│   ├── core/              # Config, DB, logging
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── main.py            # Application entrypoint
├── tests/                 # Integration tests
├── .env.example
├── Dockerfile
├── .dockerignore
├── entrypoint.sh
├── Makefile
├── pyproject.toml
└── uv.lock
```

---

## Architecture Overview

* **Routes (`api/`)** → Handle HTTP requests/responses
* **Services (`services/`)** → Business logic + DB interaction
* **Models (`models/`)** → Database schema (SQLAlchemy)
* **Schemas (`schemas/`)** → Request/response validation
* **Core (`core/`)** → Configuration, DB setup, logging

This separation keeps the codebase modular, testable, and maintainable.

---

## Prerequisites

Ensure the following tools are installed:

* Python 3.14+
* uv (Python package manager)
* Docker
* Make
* PostgreSQL (only for local non-Docker setup)
* (Optional) Node.js (for running Postman collections via Newman)

---

## Local Setup

```bash
cd student-api
make install
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/students_db
ENV=dev
```

---

## Makefile Workflow

Run the following commands **in order** when setting up the project locally:

### 1. Install dependencies

```bash
make install
```

### 2. Run database migrations

```bash
make makemigration msg="init"
make upgrade
```

### 3. Start the application

Development mode (auto-reload):

```bash
make dev
```

Production mode:

```bash
make run
```

---

### Other useful commands

```bash
make test        # Run tests
make downgrade   # Rollback last migration
make history     # View migration history
make current     # Show current DB revision
```

---

## Run the Application

### Development mode (auto-reload)

```bash
make dev
```

### Production mode

```bash
make run
```

Access the app:

* API: http://localhost:8000
* Docs (dev only): http://localhost:8000/docs

---

## Tests

```bash
make test
```

Tests use `testcontainers` to spin up an isolated PostgreSQL instance.

---

## Docker

### Important Notes

* Ensure Docker is running
* `.env` file must exist
* Inside Docker, use the container name (`student-db`) as DB host (not `localhost`)

---

### 1. Build Image

```bash
docker build -t student-api:v0.1.0 .
```

---

### 2. Create Network

```bash
docker network create student-network
```

---

### 3. Run PostgreSQL

```bash
docker run -d \
  --name student-db \
  --network student-network \
  -e POSTGRES_USER=<user-name> \
  -e POSTGRES_PASSWORD=<password> \
  -e POSTGRES_DB=<db-name> \
  postgres:15
```

---

### 4. Configure Environment

Create `.env`:

```env
DATABASE_URL=postgresql://user-name:password@student-db:5432/db-name
ENV=dev
```

---

### 5. Run API Container

```bash
docker run -d \
  --name student-api \
  --network student-network \
  --env-file .env \
  -p 8000:8000 \
  student-api:v0.1.0
```

---

### 6. Migrations

Migrations are automatically handled by `entrypoint.sh`:

* Waits for database readiness
* Runs Alembic migrations

---

### 7. Access API

* API: http://localhost:8000
* Docs (dev only): http://localhost:8000/docs

---

## Postman

```bash
npm install -g newman
newman run postman/Student-API.postman_collection.json
```

---

## Important Notes

* Do **not use `localhost` inside Docker**
* Always use container name (`student-db`)
* Environment variables must be injected via:

  ```
  --env-file .env
  ```
* Database readiness is handled via `pg_isready` using `DATABASE_URL`
* CLI tools (alembic, fastapi) are available via `.venv`

---

## Cleanup

```bash
docker stop student-api student-db
docker rm student-api student-db
docker network rm student-network
```
