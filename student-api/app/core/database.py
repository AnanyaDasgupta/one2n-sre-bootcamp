from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Build the SQLAlchemy engine from the configured database URL.
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

# SessionLocal creates a new database session for each request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is inherited by all ORM models so SQLAlchemy can track them.
Base = declarative_base()


def get_db():
    # FastAPI dependency that opens a session and closes it after the request.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
