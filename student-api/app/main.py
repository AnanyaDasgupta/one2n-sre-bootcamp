from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.student_routes import router as student_router
import app.core.logger

from app.core.database import engine, Base


# Run setup code once when the application starts.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables before the app begins handling requests.
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup code can be added here later if needed.


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    # Simple route to confirm that the API is reachable.
    return {"message": "Welcome to the Student API!"}


@app.get("/healthcheck")
def healthcheck():
    # Lightweight endpoint used to verify service health.
    return {"status": "ok"}


# Register all student endpoints with the application.
app.include_router(student_router)
