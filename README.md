# Student REST API (SRE Bootcamp)

## 📌 Overview

This project implements a simple REST API for managing student records.
It is designed following **12-Factor App principles** and focuses on production-ready practices such as configuration management, logging, and database migrations.

---

## 🚀 Features

* CRUD operations for students
* Versioned API (`/api/v1`)
* Healthcheck endpoint
* Database persistence
* Environment-based configuration
* Logging with levels
* Database migrations
* Unit tests

---

## 🧱 Tech Stack

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* uv (Package Manager)

---

## 📂 Project Structure

```
student-api/
├── app/
│   ├── config.py
│   ├── main.py
│   └── ...
├── tests/
│   └── test_health.py
├── .env
├── .env.example
├── .python-version
├── .venv/
├── pyproject.toml
├── uv.lock
└── Makefile
---

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.14+
* uv package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd one2n-sre-bootcamp
   ```

2. **Navigate to the API directory**
   ```bash
   cd student-api
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   make run
   ```

6. **Run tests**
   ```bash
   make test
   ```

---

### Base URL

```
/api/v1
```

---

### 1. Healthcheck

**GET /healthcheck**

Response:

```json
{ "status": "ok" }
```

---

### 2. Create Student

**POST /api/v1/students**

Request:

```json
{
  "name": "John Doe",
  "age": 20,
  "email": "john@example.com"
}
```

Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "age": 20,
  "email": "john@example.com"
}
```

---

### 3. Get All Students

**GET /api/v1/students**

---

### 4. Get Student by ID

**GET /api/v1/students/{id}**

---

### 5. Update Student

**PUT /api/v1/students/{id}**

---

### 6. Delete Student

**DELETE /api/v1/students/{id}**

---

## 🗄️ Data Model

Student:

```
id: integer (primary key)
name: string
age: integer
email: string (unique)
```

---

## ⚙️ Configuration

All configuration is managed via environment variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/students
PORT=8000
LOG_LEVEL=info
```

---

## 🛠️ Setup & Installation

### 1. Clone Repository

```bash
git clone <repo-url>
cd student-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

### Run Migrations

```bash
alembic upgrade head
```

---

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

App will run on:

```
http://localhost:8000
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## ⚡ Makefile Commands

```bash
make run        # start server
make test       # run tests
make migrate    # apply migrations
```

---

## 📬 Postman Collection

A Postman collection is included in the repository for testing all endpoints.

---

## 🪵 Logging

* Logs are written to stdout
* Log level is controlled via `LOG_LEVEL`
* Includes request and error logging

---




