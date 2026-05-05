import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient


IS_CI = os.getenv("CI") == "true"


@pytest.fixture(scope="session")
def engine():
    """
    Creates SQLAlchemy engine:
    - CI: uses DATABASE_URL from environment (GitHub Actions / act)
    - Local: spins up Postgres via testcontainers
    """

    postgres = None

    if IS_CI:
        database_url = os.environ["DATABASE_URL"]
    else:
        from testcontainers.postgres import PostgresContainer

        postgres = PostgresContainer("postgres:15")
        postgres.start()
        database_url = postgres.get_connection_url()

    engine = create_engine(database_url)

    # Create schema once per test session
    Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()

    if postgres:
        postgres.stop()


@pytest.fixture(scope="function")
def db(engine):
    """
    Creates a fresh DB session per test.
    Wraps each test in a transaction rollback.
    """
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()

    if transaction.is_active:
        transaction.rollback()

    connection.close()


@pytest.fixture
def client(db):
    """
    FastAPI test client with DB override.
    """

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
