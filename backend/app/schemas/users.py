from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr
    work_location: str | None = None
    home_location: str | None = None
    bio: str | None = None 
    gender: str | None = None
    
class UpdateUser(BaseModel):
    name: str | None = None
    work_location: str | None = None
    home_location: str | None = None
    bio: str  | None = None
    gender: str | None = None
    @field_validator("name","work_location","home_location")
    @classmethod
    def validate_feild(cls, value):
        if value is None:
            raise ValueError("Field cannot be null")
        if not value.strip():
            raise ValueError("Field cannot be blank")
        return value
    @field_validator("bio","gender")
    @classmethod
    def validate_bio_gender(cls, value):
        if value is None:
            raise ValueError("Field cannot be null")
        if value != "" and not value.strip():
            raise ValueError("Field cannot be whitespace")
        return value
    
class ShowUser(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    gender: str | None = None
    bio: str  | None = None
    work_location: str | None = None
    home_location: str  | None = None
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    identifier: str
    password: str