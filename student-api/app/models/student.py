from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class Student(Base):
    # SQLAlchemy model representing a student in the database
    __tablename__ = "students"

    # Primary key for the student record
    id = Column(Integer, primary_key=True, index=True)
    # Student's full name
    name = Column(String, nullable=False)
    # Student's age in years
    age = Column(Integer, nullable=False)

    # Optional email field for the student
    email = Column(String, nullable=True)

    # Optional phone number field for the student
    phone_number = Column(String, nullable=True)

    # Optional address field for the student
    address = Column(String, nullable=True)

    # Optional company field for the student
    company = Column(String, nullable=True)

    # Timestamp when the record was created
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # Timestamp when the record was last updated
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
