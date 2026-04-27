import os

from fastapi import FastAPI

from app.api.v1.student_routes import router as student_router
from app.core.logger import configure_logging
from app.routes.system_routes import router as system_router

# Configure application logging
configure_logging()

# Create FastAPI application instance with metadata
app = FastAPI(
    title="Student API",
    description="API for managing students",
    version="1.0.0",
    docs_url="NONE" if os.getenv("ENV") == "prod" else "/docs",
    redoc_url="NONE" if os.getenv("ENV") == "prod" else "/redoc",
)

# Include system routes (health check, root)
app.include_router(system_router)
# Include student CRUD routes
app.include_router(student_router)
