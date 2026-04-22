from fastapi import FastAPI
from app.api.v1.students import router as student_router
import app.core.logger

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Student API!"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(student_router)