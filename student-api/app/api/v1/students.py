from fastapi import APIRouter, HTTPException
from app.models.student import StudentCreate, StudentResponse
from app.services import student_service

router = APIRouter(prefix="/api/v1/students", tags=["students"])


@router.post("", response_model=StudentResponse, status_code=201)
def create(student: StudentCreate):
    return student_service.create_student(student)


@router.get("", response_model=list[StudentResponse])
def get_all():
    return student_service.get_all_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get(student_id: int):
    student = student_service.get_student_by_id(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update(student_id: int, data: StudentCreate):
    student = student_service.update_student(student_id, data)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


@router.delete("/{student_id}", status_code=204)
def delete(student_id: int):
    success = student_service.delete_student(student_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )