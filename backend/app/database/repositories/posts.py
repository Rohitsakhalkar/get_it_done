from app.database.models import Post, User
from app.schemas.posts import CreatePosts, ShowPosts, UpdatePost
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

def create_post(db: Session, post: CreatePosts, current_user: User):
    
    db_post = Post(
        user_id = current_user.id,
        caption = post.caption
    )

    db.add(db_post)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't create a post")
    show_post = ShowPosts(
        id = db_post.id,
        name = current_user.name,
        username = current_user.username,
        caption = db_post.caption,
        created_at = db_post.created_at,
        updated_at = db_post.updated_at
    )
    return show_post

def show_posts(db:Session ,limit: int, offset: int):
    posts_list = []
    try:
        posts = (db.query(User,Post)
             .join(Post, User.id == Post.user_id)
             .order_by(Post.id.desc())
             .limit(limit)
             .offset(offset)
             .all())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal Server error")
    
    for user,post in posts:
        user_post = ShowPosts(
            id = post.id,
            name = user.name,
            username = user.username,
            caption = post.caption,
            created_at = post.created_at,
            updated_at = post.updated_at
        )
        posts_list.append(user_post)
    return posts_list

def post_delete(db: Session, post_id: int, current_user: User):
    try:
        post = (db.query(Post)
            .filter(Post.id == post_id)
            .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if post is None:
        raise HTTPException(status_code = 404, detail = "Post doesn't exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "you don't have the permission to delete this post")
    
    db.delete(post)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't delete post")

def post_update(post_id: int, update_data: UpdatePost, db: Session, current_user: User):
    update_data = update_data.model_dump(exclude_unset = True)
    if not update_data:
        raise HTTPException(status_code = 400, detail = "empty json")
    try:
        post = (db.query(Post)
                .filter(Post.id == post_id)
                .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    if post is None:
        raise HTTPException(status_code = 404 , detail = "Error post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code = 403 ,detail = "you don't have the permission to update this post")
    
    if update_data.get('caption') is None:
        raise HTTPException(status_code = 400, detail = "field is empty or null")
    post.caption = update_data.get("caption")
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail = "field is empty or null")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't update post" )
    
    post = ShowPosts(
        id = post.id,
        name = current_user.name,
        username = current_user.username,
        caption = post.caption,
        created_at = post.created_at,
        updated_at = post.updated_at
    )
    return post

def get_post(post_id: int,db: Session):
    try:
        result = (db.query(Post,User)
              .join(User, User.id == Post.user_id)
              .filter(Post.id == post_id)
              .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    if result is None:
        raise HTTPException(status_code = 404, detail = "post doesn't exist")
    
    post, user = result
    response = ShowPosts(
            id = post.id,
            name = user.name,
            username = user.username,
            caption = post.caption,
            created_at = post.created_at,
            updated_at = post.updated_at
        )
    return response

def get_user_post(username: str, db:Session , limit: int, offset: int):
    try:
        user = (db.query(User.id)
            .filter(User.username == username)
            .first())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    if user is None:
        raise HTTPException(status_code = 404, detail = "user doesn't exist")
    
    try:
        result = (db.query(Post, User)
              .join(User, Post.user_id == User.id)
              .filter(User.username == username)
              .order_by(Post.id.desc())\
              .limit(limit)
              .offset(offset)
              .all())
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal server error")
    
    show_posts_list = [] 
    for post, user in result:
        response = ShowPosts(
            id = post.id,
            name = user.name,
            username = user.username,
            caption = post.caption,
            created_at = post.created_at,
            updated_at = post.updated_at
        )    
        show_posts_list.append(response)
    return show_posts_list