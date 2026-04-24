from fastapi import APIRouter


router = APIRouter(tags=["System"])


@router.get("/healthcheck")
def healthcheck():
    # Lightweight endpoint used to verify service health.
    return {"status": "ok"}


@router.get("/")
def root():
    # Simple route to confirm that the API is reachable.
    return {"message": "Welcome to the Student API!"}
