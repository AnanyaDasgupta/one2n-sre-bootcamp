# Student API

This repository contains a small FastAPI service for managing student records.
It is intended as a learning-friendly example of how a backend API is split into routes, services, schemas, models, and database configuration.

## What The App Includes

- CRUD endpoints for students
- Versioned API routes under `/api/v1`
- A health check endpoint
- SQLAlchemy-based database access
- Environment-based configuration
- Basic logging
- A simple test suite with isolated PostgreSQL integration tests

## Project Structure

```text
one2n-sre-bootcamp/
├── README.md
├── postman/
│   └── Student-API.postman_collection.json
└── student-api/
    ├── .env
    ├── .env.example
    ├── Makefile
    ├── README.md
    ├── alembic/
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    │     
    ├── app/
    │   ├── api/v1/student_routes.py
    │   ├── core/
    │   │   ├── config.py
    │   │   ├── database.py
    │   │   └── logger.py
    │   ├── models/student.py
    │   ├── schemas/student_schemas.py
    │   ├── services/student_service.py
    │   └── main.py
    ├── tests/
    │   ├── conftest.py
    │   ├── test_health.py
    │   └── test_students.py
    ├── pyproject.toml
    └── uv.lock
```

## How The Code Is Organized

- `app/main.py` creates the FastAPI app, adds startup logic, and includes routers.
- `app/api/v1/student_routes.py` defines the HTTP endpoints.
- `app/services/student_service.py` contains the database-facing business logic.
- `app/models/student.py` defines the SQLAlchemy model for the `students` table.
- `app/schemas/student_schemas.py` defines the request and response shapes.
- `app/core/database.py` creates the engine and database session dependency.
- `app/core/config.py` loads configuration from environment variables.

## Prerequisites

- Python 3.14+
- `uv`
- PostgreSQL

## Setup

From the repository root:

```bash
cd student-api
make install
```

Create a `.env` file inside `student-api/`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/students
```

## Alembic

Database migrations are managed with Alembic via Makefile targets.

Examples:

```bash
cd student-api
make makemigration msg="add students table"
make upgrade
```

To rollback the last migration:

```bash
make downgrade
```

To view migration history:

```bash
make history
```

## Run The Application

From the `student-api/` directory:

```bash
make run
```

For development with auto-reload:

```bash
make dev
```

The app runs on:

```text
http://localhost:8000
```

## Endpoints

`GET /`

```json
{
  "message": "Welcome to the Student API!"
}
```

`GET /healthcheck`

```json
{
  "status": "ok"
}
```

`POST /api/v1/students`

```json
{
  "name": "John Doe",
  "age": 20
}
```

`GET /api/v1/students`

`GET /api/v1/students/{student_id}`

`PUT /api/v1/students/{student_id}`

```json
{
  "name": "Jane Doe",
  "age": 21
}
```

`DELETE /api/v1/students/{student_id}`

## Student Model

```text
id   : integer, primary key
name : string, required
age  : integer, required
```

## Tests

The `student-api/tests` directory includes integration tests with isolated PostgreSQL fixtures.
The test suite uses `testcontainers` to spin up a temporary Postgres instance for each run.

From the `student-api/` directory:

```bash
make test
```

## Postman

A Postman collection is available at `postman/Student-API.postman_collection.json` for manual API testing.

## Newman

Install Newman globally with npm:

```bash
npm install -g newman
```

You can run the collection from the command line with Newman:

```bash
newman run postman/Student-API.postman_collection.json
```
