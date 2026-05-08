import socket

from fastapi import FastAPI

from app.api.v1.student_routes import router as student_router
from app.core.logger import configure_logging
from app.routes.system_routes import router as system_router
from app.core.config import settings

# Configure application logging
configure_logging()

print("ENV VALUE:", settings.ENV)

app = FastAPI(
    title="Student API",
    description="API for managing students",
    version="1.0.0",
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc",
)

@app.middleware("http")
async def add_instance_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Instance-ID"] = socket.gethostname()
    print(f"Response status: {response.status_code}")
    return response

@app.get("/instance")
async def get_instance():
    return {"hostname": socket.gethostname()}

app.include_router(system_router)
app.include_router(student_router)
