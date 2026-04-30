from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.student_schemas import StudentCreate, StudentResponse
from app.services import student_service

# API router for student-related endpoints
router = APIRouter(prefix="/api/v1/students", tags=["Students"])


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    # Create a new student record
    return student_service.create_student(db, data)


@router.get(
    "",
    response_model=list[StudentResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_students(db: Session = Depends(get_db)):
    # Retrieve all student records
    return student_service.get_all_students(db)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    # Retrieve a specific student by ID
    return student_service.get_student_or_404(db, student_id)


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
)
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    # Update an existing student record
    return student_service.update_student(db, student_id, data)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    # Delete a student record by ID
    student_service.delete_student(db, student_id)
