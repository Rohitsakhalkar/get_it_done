from app.database.models import User
from app.schemas.users import ShowUser, UserCreate
from app.security import hash_password
from fastapi import HTTPException
from sqlalchemy import or_ 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def create_user(db,user: UserCreate):
    Exisiting_user = db.query(User).filter(or_(User.username == user.username , User.email == user.email)).first()
    if Exisiting_user is not None:
        raise HTTPException(status_code = 409 , detail = "username or email already exist")
    hashed_password = hash_password(user.password)
    db_user = User(
        name = user.name,
        username = user.username,
        password_hash = hashed_password,
        email = user.email,
        work_location = user.work_location,
        home_location = user.home_location,
        bio = user.bio,
        gender = user.gender
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409, detail = "username or email already exist")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500 , detail = "user registration failed")
    response =  ShowUser(
        id = db_user.id,
        name = db_user.name,
        username = db_user.username,
        email = db_user.email,
        gender = db_user.gender,
        bio = db_user.bio,
        home_location = db_user.home_location,
        work_location = db_user.work_location,
        created_at = db_user.created_at,
        updated_at = db_user.updated_at
    ) 
    return response


