from fastapi import FastAPI

from app.api.v1.student_routes import router as student_router
from app.core.logger import configure_logging
from app.routes.system_routes import router as system_router


configure_logging()

app = FastAPI()

app.include_router(system_router)
app.include_router(student_router)
