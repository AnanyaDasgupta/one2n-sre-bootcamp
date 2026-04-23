import logging
from sqlalchemy.orm import Session
from app.models.student import Student

logger = logging.getLogger(__name__)


def create_student(db: Session, data):
    logger.info(f"Creating student: {data.name}")

    student = Student(
        name=data.name,
        age=data.age
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_all_students(db: Session):
    logger.info("Fetching all students")
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        logger.warning(f"Student {student_id} not found")

    return student


def update_student(db: Session, student_id: int, data):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        logger.warning(f"Student {student_id} not found for update")
        return None

    student.name = data.name
    student.age = data.age

    db.commit()
    db.refresh(student)

    logger.info(f"Updated student {student_id}")

    return student


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        logger.warning(f"Student {student_id} not found for deletion")
        return False

    db.delete(student)
    db.commit()

    logger.info(f"Deleted student {student_id}")
    return True