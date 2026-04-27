from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.core.database import Base

# Alembic configuration object
config = context.config

# Set the database URL from application settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configure logging if config file exists
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for migrations (SQLAlchemy models)
target_metadata = Base.metadata


def run_migrations_offline():
    # Run migrations in offline mode (generate SQL without connecting to DB)
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Run migrations in online mode (connect to DB and execute)
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Execute migrations based on offline/online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
