from pydantic import BaseModel, field_validator
from datetime import datetime

class CreatePosts(BaseModel):
    caption: str
    @field_validator("caption")
    @classmethod
    def validate_caption(cls,value):
        if value is None:
            raise ValueError("Field cannot be null")
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value
    
class ShowPosts(BaseModel):
    id: int
    user_id: int
    name: str
    username: str
    caption: str
    created_at: datetime
    updated_at: datetime

class UpdatePost(BaseModel):
    caption: str | None = None
    @field_validator("caption")
    @classmethod
    def validate_caption(cls,value):
        if value is None:
            raise ValueError("Field cannot be null")
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value