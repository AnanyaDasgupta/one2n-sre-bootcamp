import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.main import app
from fastapi.testclient import TestClient
from app.core.database import get_db


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db(engine):
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
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()