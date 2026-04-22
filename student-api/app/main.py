from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI()

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# In-memory store
# ----------------------------
students = {}
counter = 1

# ----------------------------
# Schemas
# ----------------------------
class StudentCreate(BaseModel):
    name: str
    age: int


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int


# ----------------------------
# Healthcheck
# ----------------------------
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


# ----------------------------
# Create student
# ----------------------------
@app.post("/api/v1/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    global counter

    logger.info(f"Creating student: {student.name}")

    new_student = {
        "id": counter,
        "name": student.name,
        "age": student.age,
    }

    students[counter] = new_student
    counter += 1

    return new_student


# ----------------------------
# Get all students
# ----------------------------
@app.get("/api/v1/students", response_model=list[StudentResponse])
def get_students():
    logger.info("Fetching all students")
    return list(students.values())


# ----------------------------
# Get student by ID
# ----------------------------
@app.get("/api/v1/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    student = students.get(student_id)

    if not student:
        logger.warning(f"Student {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# ----------------------------
# Update student
# ----------------------------
@app.put("/api/v1/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentCreate):
    student = students.get(student_id)

    if not student:
        logger.warning(f"Student {student_id} not found for update")
        raise HTTPException(status_code=404, detail="Student not found")

    student["name"] = data.name
    student["age"] = data.age

    logger.info(f"Updated student {student_id}")

    return student


# ----------------------------
# Delete student
# ----------------------------
@app.delete("/api/v1/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    if student_id not in students:
        logger.warning(f"Student {student_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Student not found")

    del students[student_id]

    logger.info(f"Deleted student {student_id}")

    return