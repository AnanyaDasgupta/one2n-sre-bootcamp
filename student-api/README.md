# Student API

This service is a small FastAPI application for managing student records.
It is organized as a simple layered backend so it is easy to follow the full
request flow from HTTP route to database row.

## What This Project Does

- Exposes a REST API for creating, reading, updating, and deleting students
- Uses FastAPI for routing and request validation
- Uses SQLAlchemy ORM for database access
- Reads configuration from environment variables and `.env`
- Creates the `students` table automatically when the app starts

## Tech Stack

- Python 3.14+
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- `uv` for dependency management
- `pytest` for tests

## Project Layout

```text
student-api/
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
│   └── test_health.py
├── .env.example
├── Makefile
├── pyproject.toml
└── uv.lock
```

## End-To-End Workflow

This is the runtime flow when the service starts and handles requests.

### 1. Application startup

`app/main.py` is the entrypoint for Uvicorn.

When the app starts:

- `configure_logging()` runs first and configures the root logger using `LOG_LEVEL`
- FastAPI is created with a lifespan handler
- Inside the lifespan startup block, `Base.metadata.create_all(bind=engine)` runs
- SQLAlchemy uses the configured `DATABASE_URL` to connect to PostgreSQL
- If the `students` table does not exist, SQLAlchemy creates it before serving traffic

### 2. Request enters FastAPI

When a client calls an endpoint such as `POST /api/v1/students`:

- FastAPI matches the request to a route in `app/api/v1/student_routes.py`
- The request body is validated against a Pydantic schema from `app/schemas/student_schemas.py`
- FastAPI resolves the `get_db()` dependency from `app/core/database.py`
- `get_db()` opens a SQLAlchemy session for that request

### 3. Route hands work to the service layer

The route function stays thin and delegates database work to
`app/services/student_service.py`.

That service layer:

- creates ORM objects
- queries the database
- updates existing rows
- deletes rows
- commits transactions when needed

### 4. Service talks to the model

`app/models/student.py` defines the `Student` ORM model:

- `id`: integer primary key
- `name`: required string
- `age`: required integer

The service layer queries and persists this model through the SQLAlchemy session.

### 5. Response is returned

Before FastAPI sends the response:

- ORM objects are converted into `StudentResponse`
- missing records become `404` responses in the route layer
- successful deletes return `204 No Content`
- the database session is closed automatically in the `finally` block of `get_db()`

## File-By-File Responsibilities

### `app/main.py`

- bootstraps logging
- creates the FastAPI app
- defines `/` and `/healthcheck`
- registers the student router
- creates database tables on startup

### `app/core/config.py`

- loads `DATABASE_URL`
- loads `LOG_LEVEL`
- reads from `.env`

### `app/core/database.py`

- creates the SQLAlchemy engine
- creates `SessionLocal`
- defines `Base` for ORM models
- provides `get_db()` as a FastAPI dependency

### `app/core/logger.py`

- configures the global logging format and log level

### `app/api/v1/student_routes.py`

- defines versioned student endpoints under `/api/v1/students`
- validates input through schemas
- maps missing resources to HTTP 404

### `app/schemas/student_schemas.py`

- `StudentCreate` is used for create and update payloads
- `StudentResponse` is used for API responses

### `app/services/student_service.py`

- contains the CRUD logic
- commits database writes
- refreshes ORM objects after inserts and updates
- logs key actions

### `tests/test_health.py`

- verifies that `/healthcheck` returns `200`
- checks the JSON response body

## Local Setup

From the repository root:

```bash
cd student-api
make install
```

Or directly with `uv`:

```bash
uv sync
```

## Environment Variables

Create a `.env` file inside `student-api/`.

Example:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/students
PORT=8000
LOG_LEVEL=INFO
```

Meaning:

- `DATABASE_URL`: PostgreSQL connection string used by SQLAlchemy
- `PORT`: local port used by the `Makefile` run commands
- `LOG_LEVEL`: logging verbosity such as `DEBUG`, `INFO`, or `WARNING`

## Running The Service

Production-like local run:

```bash
make run
```

Development mode with auto-reload:

```bash
make dev
```

The API will be available at:

```text
http://localhost:8000
```

## API Endpoints

### Health and root

- `GET /`
- `GET /healthcheck`

Example health response:

```json
{
  "status": "ok"
}
```

### Student CRUD

- `POST /api/v1/students`
- `GET /api/v1/students`
- `GET /api/v1/students/{student_id}`
- `PUT /api/v1/students/{student_id}`
- `DELETE /api/v1/students/{student_id}`

Create or update payload:

```json
{
  "name": "Jane Doe",
  "age": 21
}
```

Create response shape:

```json
{
  "id": 1,
  "name": "Jane Doe",
  "age": 21
}
```

## Testing

Run the test suite with:

```bash
make test
```

This currently includes a health check test in `tests/test_health.py`.

## Logging Behavior

Logging is configured once on startup.

- log level comes from `LOG_LEVEL`
- logs use a timestamped format
- service functions log create, read, update, and delete activity
- SQLAlchemy engine logging is enabled with `echo=True`, so SQL statements are printed too

## Current Caveats

- Database tables are created with `Base.metadata.create_all(...)` during app startup
- The `Makefile` mentions migration-related targets, but the repository does not currently contain a complete Alembic source setup
- Because of that, the current workflow is schema creation on startup rather than migration-driven schema management

## Quick Request Trace

For `POST /api/v1/students`, the flow is:

1. Uvicorn sends the request to FastAPI.
2. FastAPI matches the route in `student_routes.py`.
3. The JSON body is validated as `StudentCreate`.
4. `get_db()` opens a SQLAlchemy session.
5. `student_service.create_student()` builds a `Student` model.
6. The row is inserted and committed to PostgreSQL.
7. FastAPI serializes the ORM object into `StudentResponse`.
8. The session is closed after the response is sent.
