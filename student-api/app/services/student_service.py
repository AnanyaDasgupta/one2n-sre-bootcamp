import logging

logger = logging.getLogger(__name__)

students = {}
counter = 1


def create_student(data):
    global counter

    logger.info(f"Creating student: {data.name}")

    student = {
        "id": counter,
        "name": data.name,
        "age": data.age,
    }

    students[counter] = student
    counter += 1

    return student


def get_all_students():
    logger.info("Fetching all students")
    return list(students.values())


def get_student_by_id(student_id):
    student = students.get(student_id)

    if student is None:
        logger.warning(f"Student {student_id} not found")
        return None

    return student


def update_student(student_id, data):
    student = students.get(student_id)

    if student is None:
        logger.warning(f"Student {student_id} not found for update")
        return None

    student["name"] = data.name
    student["age"] = data.age

    logger.info(f"Updated student {student_id}")

    return student


def delete_student(student_id):
    if student_id not in students:
        logger.warning(f"Student {student_id} not found for deletion")
        return False

    del students[student_id]

    logger.info(f"Deleted student {student_id}")
    return True