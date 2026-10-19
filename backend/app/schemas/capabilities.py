from pydantic import BaseModel, field_validator

class CreateCapabilities(BaseModel):
    capability: str
    @field_validator("capability")
    @classmethod
    def validate_capability(cls,value):
        if not value.strip():
            raise ValueError("field cannot be empty")
        return value
    
class ShowCapabilities(BaseModel):
    id: int
    user_id: int
    capability: str

class ShowUserCapability(BaseModel):
    id: int
    capability: str

class UpdateUserCapability(BaseModel):
    capability: str
    @field_validator("capability")
    @classmethod
    def validate_capability(cls,value):
        if not value.strip():
            raise ValueError("field cannot be empty")
        return value