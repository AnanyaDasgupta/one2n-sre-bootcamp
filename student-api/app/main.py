from fastapi import FastAPI

from app.api.v1.student_routes import router as student_router
from app.core.logger import configure_logging
from app.routes.system_routes import router as system_router
from app.core.config import settings

# Configure application logging
configure_logging()

app = FastAPI(
    title="Student API",
    description="API for managing students",
    version="1.0.0",
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc",
)

app.include_router(system_router)
app.include_router(student_router)