from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "John Doe"})
    age: int = Field(..., json_schema_extra={"example": 21})
    email: str | None = Field(None, json_schema_extra={"example": "abc@gmail.com"})
    phone_number: str | None = Field(None, json_schema_extra={"example": "+1234567890"})
    address: str | None = Field(
        None, json_schema_extra={"example": "123 Main St, Anytown, USA"}
    )
    company: str | None = Field(None, json_schema_extra={"example": "Acme Corp"})


class StudentResponse(BaseModel):
    # Schema used when sending student data back to the client.
    id: int
    name: str
    age: int
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    company: str | None = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "John Doe",
                "age": 21,
                "email": "abc@gmail.com",
                "phone_number": "+1234567890",
                "address": "123 Main St, Anytown, USA",
                "company": "Acme Corp",
            }
        },
    }
