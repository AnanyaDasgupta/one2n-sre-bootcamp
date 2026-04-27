from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "John Doe"})
    age: int = Field(..., json_schema_extra={"example": 21})


class StudentResponse(BaseModel):
    # Schema used when sending student data back to the client.
    id: int
    name: str
    age: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {"example": {"id": 1, "name": "John Doe", "age": 21}}
    }
