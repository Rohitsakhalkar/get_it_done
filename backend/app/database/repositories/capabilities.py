from app.database.models import User, Capabilities
from app.schemas.capabilities import CreateCapabilities, ShowCapabilities, ShowUserCapability
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def create_capability(Create_Capabilty: CreateCapabilities, db, current_user):
    db_capabilities = Capabilities(
        user_id = current_user.id,
        capability = Create_Capabilty.capability
    )
    db.add(db_capabilities)
    try:
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code = 500, detail = "couldn't create user")
    show_capabilities = ShowCapabilities(
        id = db_capabilities.id,
        user_id = db_capabilities.user_id,
        capability = db_capabilities.capability
    )
    return show_capabilities

def show_user_capabilities(user_id, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User doesn't Exist")
    capabilities = db.query(Capabilities).filter(Capabilities.user_id == user_id).all()
    capabilities_list = []
    for cap in capabilities:
        show_capability = ShowUserCapability(
            id = cap.id,
            capability = cap.capability
        ) 
        capabilities_list.append(show_capability)
    return capabilities_list

def delete_capability(capability_id, db, current_user):
    capability = db.query(Capabilities).filter(Capabilities.id == capability_id).first()
    if capability is None:
        raise HTTPException(status_code = 404, detail = "capabilty does not exist")
    if current_user.id != capability.user_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized user")
    db.delete(capability)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500 , detail = "couldn't delete user")
    
    
def update_capability(capability_id, capability_data, db, current_user):
    capability = db.query(Capabilities).filter(Capabilities.id == capability_id).first()
    if capability is None:
        raise HTTPException(status_code = 404, detail = "capability does not exist")
    if current_user.id != capability.user_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized user")
    capability.capability = capability_data.capability

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500 , detail = "couldn't update user")
    
    return capability.capability