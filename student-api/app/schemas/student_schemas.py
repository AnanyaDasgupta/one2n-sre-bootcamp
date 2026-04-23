from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int

    model_config = {
        "from_attributes": True
    }