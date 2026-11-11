from app.database.models import User
from app.schemas.users import (ShowUser, 
                               UserCreate, 
                               UserLogin, 
                               UpdateUser, 
                               ShowSearchedUsers,
                               PublicProfile)
from fastapi import HTTPException
from sqlalchemy import or_ 
from sqlalchemy.exc import (IntegrityError, 
                            SQLAlchemyError)
from app.security import (hash_password, 
                          create_access_token, 
                          verify_password)
from sqlalchemy.orm import Session

def create_user(db: Session, user: UserCreate):
    try:
        Exisiting_user = (db.query(User)
                      .filter(or_(User.username == user.username,
                                   User.email == user.email))
                      .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if Exisiting_user:
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
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409, detail = "username or email already exist")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500 , detail = "user registration failed")
    db.refresh(db_user)
    response = {
        "message":"User created successfully",
        "id": db_user.id,
        "username": db_user.username
    }
    return response

def user_login(db: Session, user: UserLogin):
    try:
        db_user = (db.query(User)
               .filter(or_(User.username == user.identifier, 
                           User.email == user.identifier))
               .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if db_user is None:
        raise HTTPException(status_code = 401 ,detail = "Unauthorized login")
    
    if verify_password(user.password,db_user.password_hash):
        data = {
            "sub": str(db_user.id)
        }
        return create_access_token(data)
    else:
        raise HTTPException(status_code = 401, detail = "Unauthorized login")
    
def show_user(id: int, db: Session):
    try:
        user = (db.query(User)
            .filter(User.id == id)
            .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "internal server error")
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    response = PublicProfile(
        id = user.id,
        name = user.name,
        username = user.username,
        gender = user.gender,
        bio = user.bio,
        home_location = user.home_location,
        work_location = user.work_location,
        created_at = user.created_at,
        updated_at = user.updated_at
    ) 
    return response

def update_user_data(user: UpdateUser, db: Session, current_user: User):

    update_user = user.model_dump(exclude_unset = True)

    if not update_user:
        raise HTTPException(status_code = 400, detail = "empty json")
    for fields, values in update_user.items():
        setattr(current_user, fields, values)
    try:
        db.commit()
        db.refresh(current_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "User updation failed")
    
    response = show_user(current_user.id, db)
    return response

def search_users(identifier: str, db: Session, limits: int, offset: int):
    try:
        users = (db.query(User)
            .filter(or_(User.name.ilike(f"%{identifier}%"), 
                        User.username.ilike(f"%{identifier}%")))
            .order_by(User.created_at.desc(), User.id.desc())
            .limit(limits)
            .offset(offset)
            .all())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    user_list = []
    for user in users:
         response = ShowSearchedUsers(
                id = user.id,
                name = user.name,
                username = user.username,
            ) 
         user_list.append(response)
    return user_list

def search_user(username: str, db: Session):
    try:
        user = db.query(User).filter(User.username == username).first()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if user is None:
        raise HTTPException(status_code = 404, detail = "user does not exist")
    
    response = PublicProfile(
            id = user.id,
            name = user.name,
            username = user.username,
            gender = user.gender,
            bio = user.bio,
            home_location = user.home_location,
            work_location = user.work_location,
            created_at = user.created_at,
            updated_at = user.updated_at
        ) 
    return response