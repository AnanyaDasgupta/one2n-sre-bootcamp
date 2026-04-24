import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student

logger = logging.getLogger(__name__)


def create_student(db: Session, data):
    # Convert the validated request data into a SQLAlchemy model instance.
    logger.info(f"Creating student: {data.name}")

    student = Student(
        name=data.name,
        age=data.age
    )

    # Persist the row, then refresh it so generated values like id are available.
    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_all_students(db: Session):
    # Return all student rows as ORM objects.
    logger.info("Fetching all students")
    return db.query(Student).all()


def get_student_or_404(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return student


def get_student_by_id(db: Session, student_id: int):
    # Look up a single row by primary key.
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        logger.warning(f"Student {student_id} not found")
    return student


def update_student(db: Session, student_id: int, data):
    # Load the existing row before applying updates.
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found for update")

    # Replace the stored values with the new payload values.
    student.name = data.name
    student.age = data.age

    # Commit the changes and reload the row from the database.
    db.commit()
    db.refresh(student)

    logger.info(f"Updated student {student_id}")

    return student


def update_student_or_404(db: Session, student_id: int, data):
    student = get_student_or_404(db, student_id)
    student.name = data.name
    student.age = data.age

    db.commit()
    db.refresh(student)

    logger.info(f"Updated student {student_id}")
    return student


def delete_student(db: Session, student_id: int):
    # Fetch the row first so we know whether there is anything to delete.
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        logger.warning(f"Student {student_id} not found for deletion")
        return False

    # Delete the row permanently and commit the transaction.
    db.delete(student)
    db.commit()

    logger.info(f"Deleted student {student_id}")
    return True


def delete_student_or_404(db: Session, student_id: int):
    student = get_student_or_404(db, student_id)
    db.delete(student)
    db.commit()

    logger.info(f"Deleted student {student_id}")
