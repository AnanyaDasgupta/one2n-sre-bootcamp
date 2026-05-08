# Declare commands (not files)
.PHONY: install run dev test lint format \
        makemigration upgrade downgrade current heads history reset-db \
        docker-build docker-network docker-db docker-run docker-migrate docker-stop docker-clean \
        postman-test

# Load environment variables if .env exists
ifneq (,$(wildcard .env))
include .env
export
endif

PORT ?= 8000
IMAGE_NAME ?= student-api
NETWORK_NAME ?= student-network
DB_CONTAINER ?= student-db
API_CONTAINER ?= student-api
TAG ?= latest # local testing uses latest. CI will inject semver tagging

# ----------------------
# Install dependencies
# ----------------------
install:
	uv sync

# ----------------------
# Run app (local)
# ----------------------
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $(PORT)

# ----------------------
# Testing & linting
# ----------------------
test:
	PYTHONPATH=. uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

# ----------------------
# Alembic (local DB)
# ----------------------
makemigration:
	uv run alembic revision --autogenerate -m "$(msg)"

upgrade:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

current:
	uv run alembic current

heads:
	uv run alembic heads

history:
	uv run alembic history --verbose

reset-db:
ifndef ENV
	$(error ENV not set. Use ENV=dev)
endif
ifeq ($(ENV),prod)
	$(error Cannot reset production database)
endif
	uv run alembic downgrade base
	uv run alembic upgrade head

# ----------------------
# Docker
# ----------------------

# Build image
docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Create network
docker-network:
	docker network create $(NETWORK_NAME) || true

# Run Postgres container
docker-db:
	docker run -d \
		--name $(DB_CONTAINER) \
		--network $(NETWORK_NAME) \
		-e POSTGRES_USER=student_user \
		-e POSTGRES_PASSWORD=password123 \
		-e POSTGRES_DB=students_db \
		postgres:15

# Run API container
docker-run:
	docker run -d \
		--name $(API_CONTAINER) \
		--network $(NETWORK_NAME) \
		--env-file .env \
		-p $(PORT):8000 \
		$(IMAGE_NAME):$(TAG)

# Run migrations inside container
docker-migrate:
	docker exec -it $(API_CONTAINER) alembic upgrade head

# Stop containers
docker-stop:
	docker stop $(API_CONTAINER) $(DB_CONTAINER) || true

# Remove containers + network
docker-clean:
	docker rm $(API_CONTAINER) $(DB_CONTAINER) || true
	docker network rm $(NETWORK_NAME) || true


# ----------------------
# Docker (local dev)
# ----------------------

build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

up:
	docker-compose up --build -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose down && docker-compose up --build -d

ps:
	docker-compose ps

cleanup:
	docker-compose down -v


# ---------
# Vagrant 
# ---------

vm-up:
	vagrant up

vm-provision:
	vagrant provision

vm-restart:
	vagrant reload

vm-ssh:
	vagrant ssh


# ----------------------
# CI Targets (stage-based)
# ----------------------

# Build stage (dependency + docker build)
ci-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Lint stage (static analysis)
ci-lint:
	uv run ruff check .
	uv run ruff format --check .

# Test stage (unit + integration + API)
ci-test:
	PYTHONPATH=. uv run pytest -v

# Full CI pipeline (order enforced)
ci: ci-lint ci-test ci-build

# Test the docker container instead of local code to validate the image works in isolation. We run the container, wait for it to be healthy, then stop and remove it.
ci-smoke:
	docker run -d \
		--name smoke-test \
		-p 8000:8000 \
		--env-file .env \
		$(IMAGE_NAME):$(TAG); \
	for i in $$(seq 1 30); do \
		curl -sf http://localhost:8000/healthcheck && echo "ready" && break || sleep 1; \
	done; \
	curl -sf http://localhost:8000/healthcheck; \
	docker stop smoke-test; \
	docker rm smoke-test;

# ----------------------
# Postman tests
# ----------------------
postman-test:
	newman run ../postman/Student-API.postman_collection.json \
		-e ../postman/local.postman_environment.json