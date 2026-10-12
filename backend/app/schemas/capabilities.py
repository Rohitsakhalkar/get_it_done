from pydantic import BaseModel

class CreateCapabilities(BaseModel):
    capability: str

class ShowCapabilities(BaseModel):
    id: int
    user_id: int
    capability: str

class ShowUserCapability(BaseModel):
    capability: str