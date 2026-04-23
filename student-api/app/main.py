from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.student_routes import router as student_router
import app.core.logger

from app.core.database import engine, Base
from app.models import student  # register models


# 👇 Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (optional)


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Welcome to the Student API!"}


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


app.include_router(student_router)