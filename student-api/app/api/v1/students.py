from fastapi import APIRouter, HTTPException
from app.models.student import StudentCreate, StudentResponse
from app.services import student_service

# API router for student-related endpoints, prefixed with /api/v1/students
router = APIRouter(prefix="/api/v1/students", tags=["students"])


# Create a new student and return the created student with an assigned ID. Calls the student_service to handle the creation logic.
@router.post("", response_model=StudentResponse, status_code=201)
def create(student: StudentCreate):
    return student_service.create_student(student)


# Return a list of all students. Calls the student_service to fetch all students from the in-memory store.
@router.get("", response_model=list[StudentResponse])
def get_all():
    return student_service.get_all_students()


# Return a single student by ID. If the student is not found, raise a 404 HTTPException. Calls the student_service to fetch the student by ID.
@router.get("/{student_id}", response_model=StudentResponse)
def get(student_id: int):
    student = student_service.get_student_by_id(student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


# Update an existing student by ID. If the student is not found, raise a 404 HTTPException. Calls the student_service to update the student and return the updated student.
@router.put("/{student_id}", response_model=StudentResponse)
def update(student_id: int, data: StudentCreate):
    student = student_service.update_student(student_id, data)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )

    return student


# Delete a student by ID. If the student is not found, raise a 404 HTTPException. Calls the student_service to delete the student and return a 204 No Content response if successful.
@router.delete("/{student_id}", status_code=204)
def delete(student_id: int):
    success = student_service.delete_student(student_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found"
        )