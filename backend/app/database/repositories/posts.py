from app.database.models import Post, User
from app.schemas.posts import CreatePosts, ShowPosts, UpdatePost
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def create_post(db, post: CreatePosts, current_user):
    
    db_post = Post(
        user_id = current_user.id,
        caption = post.caption
    )
    db.add(db_post)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't create a user")
    show_post = ShowPosts(
        id = db_post.id,
        user_id = db_post.user_id,
        name = current_user.name,
        username = current_user.username,
        caption = db_post.caption,
        created_at = db_post.created_at,
        updated_at = db_post.updated_at
    )
    return show_post

def show_posts(db, post_limit, post_offset):
    posts_list = []
    posts = db.query(User,Post).join(Post, User.id == Post.user_id).order_by(Post.id.desc()).limit(post_limit).offset(post_offset).all()
    for user,post in posts:
        user_post = ShowPosts(
            id = post.id,
            user_id = post.user_id,
            name = user.name,
            username = user.username,
            caption = post.caption,
            created_at = post.created_at,
            updated_at = post.updated_at
        )
        posts_list.append(user_post)
    return posts_list

def post_delete(db, post_id, current_user):
    post = db.query(Post).filter(Post.id == post_id).first()
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

def post_update(post_id, update_data: UpdatePost, db, current_user):
    update_data = update_data.model_dump(exclude_unset = True)
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code = 404 , detail = "Error post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code = 403 ,detail = "you don't have the permission to update this post")
    if update_data.get('caption') is None:
        raise HTTPException(status_code = 422, detail = "field is empty or null")
    post.caption = update_data.get("caption")
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail = "field is empty or null")
    
    post = ShowPosts(
        id = post.id,
        user_id = post.user_id,
        name = current_user.name,
        username = current_user.username,
        caption = post.caption,
        created_at = post.created_at,
        updated_at = post.updated_at
    )
    return post

