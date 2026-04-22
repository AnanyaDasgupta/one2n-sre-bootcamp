from pydantic import BaseModel

# Request model for creating a new student
class StudentCreate(BaseModel):
    name: str
    age: int

# Response model for returning student data, including the assigned ID
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int