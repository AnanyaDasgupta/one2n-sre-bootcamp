from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import student_service
from app.schemas.student_schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/api/v1/students", tags=["Students"])


@router.post(
    "",
    response_model=StudentResponse,
    status_code=201,
    summary="Create a new student",
    description="Creates a new student with the provided information",
)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)


@router.get(
    "",
    response_model=list[StudentResponse],
    summary="Get all students",
    description="Returns a list of all students in the database",
)
def list_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID",
    description="Returns a single student by their ID",
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return student_service.get_student_or_404(db, student_id)


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update student by ID",
    description="Updates a student's information by their ID",
)
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    return student_service.update_student_or_404(db, student_id, data)


@router.delete(
    "/{student_id}",
    status_code=204,
    summary="Delete student by ID",
    description="Deletes a student by their ID",
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_service.delete_student_or_404(db, student_id)
    return Response(status_code=204)
