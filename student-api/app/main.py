from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ----------------------------
# Healthcheck
# ----------------------------
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Student API!"}

