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

* Python 3.14+
* uv
* PostgreSQL

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

## Database Migrations (Alembic)

```bash
make makemigration msg="create students table"
make upgrade
```

Other useful commands:

```bash
make downgrade     # rollback last migration
make history       # view migration history
make current       # show current revision
```

---

## Run the Application

Production mode:

```bash
make run
```

Development mode (auto-reload):

```bash
make dev
```

Access the app:

* API: http://localhost:8000
* Docs (dev only): http://localhost:8000/docs

---

## Docker

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

### 4. Run API Container

Ensure `.env` contains:

```env
DATABASE_URL=postgresql://user-name:password@db_container-name:5432/db-name
ENV=dev
```

```bash
docker run -d \
  --name student-api \
  --network student-network \
  --env-file .env \
  -p 8000:8000 \
  student-api
```

or 

```bash
docker run -d \
  --name student-api \
  --network student-network \
  -e DATABASE_URL = <database-url>
  -p 8000:8000 \
  student-api:v0.1.0
```

---

### 5. Run Migrations

Migrations are handled by entrypoint.sh, once the container is up.

---

### 6. Access API

* API: http://localhost:8000
* Docs (dev only): http://localhost:8000/docs

---

## Tests

```bash
make test
```

Tests use `testcontainers` to spin up an isolated PostgreSQL instance.

---

## Postman

```text
postman/Student-API.postman_collection.json
```

Run with Newman:

```bash
npm install -g newman
newman run postman/Student-API.postman_collection.json
```

---

## Notes

* Inside Docker, set the db container name as the database host (not `localhost`)
* Environment variables must be injected at runtime (`--env-file`)
* Ensure DB container is ready before running migrations

---

## Cleanup

```bash
docker stop student-api student-db
docker rm student-api student-db
docker network rm student-network
```
