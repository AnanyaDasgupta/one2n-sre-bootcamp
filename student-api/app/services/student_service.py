import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student

logger = logging.getLogger(__name__)


def create_student(db: Session, data):
    logger.debug("Creating student")

    try:
        student = Student(name=data.name, age=data.age)

        db.add(student)
        db.commit()
        db.refresh(student)

        logger.info(f"Created student ID: {student.id}")
        return student

    except Exception as e:
        logger.error(f"Error creating student: {str(e)}", exc_info=True)
        db.rollback()
        raise


def get_all_students(db: Session):
    logger.debug("Fetching all students")

    try:
        students = db.query(Student).all()
        logger.info(f"Fetched {len(students)} students")
        return students

    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}", exc_info=True)
        db.rollback()
        raise


def get_student_or_404(db: Session, student_id: int):
    logger.debug(f"Looking up student ID: {student_id}")

    student = get_student_by_id(db, student_id)

    if student is None:
        logger.warning(f"Student not found: ID {student_id}")
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    logger.debug(f"Found student ID: {student_id}")
    return student


def get_student_by_id(db: Session, student_id: int):
    logger.debug(f"Querying student ID: {student_id}")
    return db.get(Student, student_id)


def update_student(db: Session, student_id: int, data):
    logger.debug(f"Updating student ID: {student_id}")

    try:
        student = get_student_or_404(db, student_id)

        student.name = data.name
        student.age = data.age

        db.commit()
        db.refresh(student)

        logger.info(f"Updated student ID: {student_id}")
        return student

    except Exception as e:
        logger.error(f"Error updating student ID {student_id}: {str(e)}", exc_info=True)
        db.rollback()
        raise


def delete_student(db: Session, student_id: int):
    logger.debug(f"Deleting student ID: {student_id}")

    try:
        student = get_student_or_404(db, student_id)

        db.delete(student)
        db.commit()

        logger.info(f"Deleted student ID: {student_id}")
        return True

    except Exception as e:
        logger.error(f"Error deleting student ID {student_id}: {str(e)}", exc_info=True)
        db.rollback()
        raise