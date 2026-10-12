from pydantic import BaseModel, EmailStr
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

