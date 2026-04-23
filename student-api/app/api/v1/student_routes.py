from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import student_service
from app.schemas.student_schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/api/v1/students")


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # FastAPI validates the body against StudentCreate before this function runs.
    return student_service.create_student(db, student)


@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    # Return every student currently stored in the database.
    return student_service.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    # Read one student and convert a missing record into an HTTP 404.
    student = student_service.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    # Update expects a full replacement payload using the same schema as create.
    student = student_service.update_student(db, student_id, data)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    # Return no content on success, or 404 if the target row does not exist.
    success = student_service.delete_student(db, student_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return
