from app.database.models import User, Capabilities
from app.schemas.capabilities import CreateCapabilities, ShowCapabilities, ShowUserCapability, UpdateUserCapability
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

def create_capability(Create_Capabilty: CreateCapabilities, db: Session, current_user: User):

    db_capabilities = Capabilities(
        user_id = current_user.id,
        capability = Create_Capabilty.capability
    )
    db.add(db_capabilities)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail = "capability already exists")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't create user")
    
    show_capabilities = ShowCapabilities(
        id = db_capabilities.id,
        user_id = db_capabilities.user_id,
        capability = db_capabilities.capability
    )
    return show_capabilities

def show_user_capabilities(user_id: int, db: Session):
    try:
        user = (db.query(User)
                .filter(User.id == user_id)
                .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if user is None:
        raise HTTPException(status_code = 404, detail = "User doesn't Exist")
    try:
        capabilities = (db.query(Capabilities)
                        .filter(Capabilities.user_id == user_id)
                        .all())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    capabilities_list = []
    for cap in capabilities:
        show_capability = ShowUserCapability(
            id = cap.id,
            capability = cap.capability
        ) 
        capabilities_list.append(show_capability)

    return capabilities_list

def delete_capability(capability_id: int, db: Session, current_user: User):
    try:
        capability = (db.query(Capabilities)
                      .filter(Capabilities.id == capability_id)
                      .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
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
    
    
def update_capability(capability_id: int, capability_data: UpdateUserCapability, db: Session, current_user: User):
    
    capability_data = capability_data.model_dump(exclude_unset = True)
    
    if not capability_data:
        raise HTTPException(status_code = 400, detail = "empty json")
    try:
        capability = (db.query(Capabilities)
                      .filter(Capabilities.id == capability_id)
                      .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if capability is None:
        raise HTTPException(status_code = 404, detail = "capability does not exist")
    
    if current_user.id != capability.user_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized user")
    
    capability.capability = capability_data.get("capability")

    try:
        db.commit()
        db.refresh(capability)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409, detail = "capabilty already Exist")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500 , detail = "couldn't update user")
    show_capabilty = ShowUserCapability(
        id = capability.id,
        capability = capability.capability
    )
    return show_capabilty