from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Student(Base):
    # ORM model mapped to the "students" table.
    __tablename__ = "students"

    # Primary key for each student record.
    id = Column(Integer, primary_key=True, index=True)
    # Student name is required.
    name = Column(String, nullable=False)
    # Student age is required.
    age = Column(Integer, nullable=False)
