from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import student_service
from app.schemas.student_schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/api/v1/students", tags=["Students"])


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)


@router.get("", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return student_service.get_student_or_404(db, student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    return student_service.update_student_or_404(db, student_id, data)


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_service.delete_student_or_404(db, student_id)
    return Response(status_code=204)
