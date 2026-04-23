from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import student_service
from app.schemas.student_schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/api/v1/students")


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)


@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, data)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = student_service.delete_student(db, student_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return