from pydantic import BaseModel
from datetime import datetime

class CreatePosts(BaseModel):
    user_id: int
    caption: str

class ShowPosts(BaseModel):
    id: int
    user_id: int
    name: str
    username: str
    caption: str
    created_at: datetime
    updated_at: datetime

class UpdatePost(BaseModel):
    caption: str
    