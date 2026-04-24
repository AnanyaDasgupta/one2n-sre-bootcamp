from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.student_routes import router as student_router
from app.core.database import Base, engine
from app.core.logger import configure_logging
from app.routes.system_routes import router as system_router


configure_logging()


# Run setup code once when the application starts.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables before the app begins handling requests.
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup code can be added here later if needed.


app = FastAPI(lifespan=lifespan)
app.include_router(system_router)
app.include_router(student_router)
