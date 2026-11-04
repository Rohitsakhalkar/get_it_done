from pydantic import BaseModel, field_validator
from datetime import datetime

class CreateTask(BaseModel):
    title: str
    description: str
    location: str
    payment: str
    @field_validator("title","location","description","payment")
    @classmethod
    def validate_fields_for_none(cls, value):
        if value is None:
            raise ValueError("field cannot be null")
        if not value.strip():
            raise ValueError("field cannot be empty")
        return value


class ShowTask(BaseModel):
    id: int
    title: str
    description: str
    name: str
    username: str
    location: str
    payment: str
    status: str
    created_at: datetime
    updated_at: datetime

class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    payment: str | None = None
    @field_validator("title","description","location","payment", mode = "before")
    @classmethod
    def validate_field(cls, value):
        if value is None:
            raise ValueError("fields cannot be null")
        if not value.strip():
            raise ValueError("fields cannot be empty")
        return value