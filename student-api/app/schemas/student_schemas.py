from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=21)


class StudentResponse(BaseModel):
    # Schema used when sending student data back to the client.
    id: int
    name: str
    age: int

    class Config:
        json_schema_extra = {"example": {"id": 1, "name": "John Doe", "age": 21}}

    # Allow FastAPI to serialize SQLAlchemy model instances into this schema.
    model_config = {"from_attributes": True}
