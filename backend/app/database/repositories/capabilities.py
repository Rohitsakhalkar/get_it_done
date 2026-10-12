from app.database.models import User, Capabilities
from app.schemas.capabilities import CreateCapabilities, ShowCapabilities, ShowUserCapability
from fastapi import HTTPException

def create_capability(user_id, Create_Capabilty: CreateCapabilities, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User does not exist")
    db_capabilities = Capabilities(
        user_id = user.id,
        capability = Create_Capabilty.capability
    )
    db.add(db_capabilities)
    db.commit()
    show_capabilities = ShowCapabilities(
        id = db_capabilities.id,
        user_id = db_capabilities.user_id,
        capability = db_capabilities.capability
    )
    return show_capabilities

def show_user_capabilities(user_id, db):
    capabilities = db.query(Capabilities).filter(Capabilities.user_id == user_id).all()
    if capabilities is None:
        raise HTTPException(status_code = 404, detail = "capabilites does not exist")
    capabilities_list = []
    for cap in capabilities:
        show_capability = ShowUserCapability(
            capability = cap.capability
        ) 
        capabilities_list.append(show_capability)
    return capabilities_list