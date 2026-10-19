from pydantic import BaseModel, field_validator
from datetime import datetime


class ShowFollowed(BaseModel):
    id: int
    followed_to: int
    followed_to_username: str
    followed_by: int
    followed_by_username: str
    created_at: datetime

class ShowFollower(BaseModel):
    follower_id: int
    follower_username: str
    follower_name: str

class ShowFollowing(BaseModel):
    following_id: int
    following_username: str
    following_name: str