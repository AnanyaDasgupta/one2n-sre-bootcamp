from pydantic import BaseModel


class StudentCreate(BaseModel):
    # Schema used for incoming create and update request bodies.
    name: str
    age: int


class StudentResponse(BaseModel):
    # Schema used when sending student data back to the client.
    id: int
    name: str
    age: int

    # Allow FastAPI to serialize SQLAlchemy model instances into this schema.
    model_config = {
        "from_attributes": True
    }
