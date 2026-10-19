from app.database.models import User
from app.schemas.users import ShowUser, UserCreate, UserLogin, UpdateUser, ShowSearchedUsers
from app.security import hash_password
from fastapi import HTTPException
from sqlalchemy import or_ 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.security import hash_password, create_access_token, verify_password

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
    
    return show_user(db_user.id, db)


def user_login(db, user: UserLogin):
    db_user = db.query(User).filter(or_(User.username == user.identifier, User.email == user.identifier)).first()
    if db_user is None:
        raise HTTPException(status_code = 401 ,detail = "Unauthorized login")
    if verify_password(user.password,db_user.password_hash):
        data = {
            "sub": str(db_user.id)
        }
        return create_access_token(data)
    else:
        raise HTTPException(status_code = 401, detail = "Unauthorized login")
    
def show_user(id: int,db):
    user = db.query(User).filter(User.id == id).first()
    response = ShowUser(
        id = user.id,
        name = user.name,
        username = user.username,
        email = user.email,
        gender = user.gender,
        bio = user.bio,
        home_location = user.home_location,
        work_location = user.work_location,
        created_at = user.created_at,
        updated_at = user.updated_at
    ) 
    return response

def update_user_data(user: UpdateUser, db, current_user):
    user = user.model_dump(exclude_unset = True)
    for fields, values in user.items():
        setattr(current_user, fields, values)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "User updation failed")
    
    return show_user(current_user.id, db)

def search_users(identifier, db, limits, offset):
    users = db.query(User).filter(or_(User.name.ilike(f"%{identifier}%"), 
                                      User.username.ilike(f"%{identifier}%") )).order_by(User.created_at.desc(), User.id.desc()).limit(limits).offset(offset).all()
    user_list = []
    for user in users:
         response = ShowSearchedUsers(
                id = user.id,
                name = user.name,
                username = user.username,
            ) 
         user_list.append(response)
    return user_list

def search_user(username, db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "user does not exist")
    response = ShowUser(
            id = user.id,
            name = user.name,
            username = user.username,
            email = user.email,
            gender = user.gender,
            bio = user.bio,
            home_location = user.home_location,
            work_location = user.work_location,
            created_at = user.created_at,
            updated_at = user.updated_at
        ) 
    return response