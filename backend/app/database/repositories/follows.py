from app.database.models import Follows, User
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.schemas.follows import  ShowFollowed, ShowFollower, ShowFollowing

def follow_user(followed_username , db, current_user):
    user = db.query(User).filter(User.username == followed_username).first()
    
    if user is None:
        raise HTTPException(status_code = 404, detail = "user doesn't exist")
    if current_user.id == user.id:
        raise HTTPException(status_code = 400, detail = "you cannot follow yourself")
    follow = db.query(Follows).filter(and_(Follows.followed_by == current_user.id, Follows.followed_to == user.id)).first()
    if follow:
        raise HTTPException(status_code = 409, detail = "you have already followed")
    db_followed = Follows(
        followed_by = current_user.id,
        followed_to = user.id
    )
    db.add(db_followed)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500 , detail = "couldn't not follow there was an error")
    except IntegrityError:
        raise HTTPException(status_code = 409, detail = "user already followed")
    db.refresh(db_followed)
    response = ShowFollowed(
        id =  db_followed.id,
        followed_by = db_followed.followed_by,
        followed_by_username = current_user.username,
        followed_to = db_followed.followed_to,
        followed_to_username = user.username,
        created_at = db_followed.created_at
    )
    return response

def unfollow_user(unfollowed_username, db, current_user):
    user = db.query(User).filter(User.username == unfollowed_username).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "user doesn't exist")
    deleted_follower = db.query(Follows).filter(and_(Follows.followed_by == current_user.id, Follows.followed_to == user.id)).first()
    if deleted_follower is None:
        raise HTTPException(status_code = 404, detail = "you don't follow this user")
    db.delete(deleted_follower)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't delete user")

def get_follower_count(username, db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "user not found")
    follower_count = db.query(Follows).filter(Follows.followed_to == user.id).count()
    
    return follower_count

def get_following_count(username, db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "user not found")
    following_count = db.query(Follows).filter(Follows.followed_by == user.id).count()

    return following_count

def get_followers(username, db, limit,offset):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "user not found")
    followers = db.query(Follows,User
                         ).filter(Follows.followed_to == user.id
                                  ).join(User, User.id == Follows.followed_by
                                         ).order_by(User.id).limit(limit).offset(offset).all()
    followers_list = []
    for follow, follow_user in followers:
        response = ShowFollower(
            follower_id = follow_user.id,
            follower_username = follow_user.username,
            follower_name = follow_user.name
        )
        followers_list.append(response)
    return followers_list

def get_followings(username, db,limit,offset):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "user not found")
    following = db.query(Follows,User
                         ).join(User, User.id == Follows.followed_to
                                ).filter(Follows.followed_by == user.id
                                         ).order_by(User.id).limit(limit).offset(offset).all()
    following_list = []
    for follow, follow_user in following:
        response = ShowFollowing(
            following_id = follow_user.id,
            following_username = follow_user.username,
            following_name = follow_user.name
        )
        following_list.append(response)
    return following_list