from app.database.models import Post, User
from app.schemas.posts import CreatePosts, ShowPosts, UpdatePost
from fastapi import HTTPException


def create_post(db, post: CreatePosts):
    user = db.query(User).filter(User.id == post.user_id).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User doesn't Exist")
    db_post = Post(
        user_id = post.user_id,
        caption = post.caption
    )
    db.add(db_post)
    db.commit()
    show_post = ShowPosts(
        id = db_post.id,
        user_id = db_post.user_id,
        name = user.name,
        username = user.username,
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

def post_delete(db, post_id):
    delete_post = db.query(Post).filter(Post.id == post_id).first()
    if delete_post is None:
        raise HTTPException(status_code = 404, detail = "Post doesn't exist")
    db.delete(delete_post)
    db.commit()
    return "deleted"

def post_update(post_id,update_data: UpdatePost,db):
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code = 404 , detail = "Error post not found")
    user = db.query(User).filter(User.id == post.user_id).first()
    if user is None:
        raise HTTPException(status_code = 404 , detail = "Error user not found")
    post.caption = update_data.caption
    db.commit()
    
    post = ShowPosts(
        id = post.id,
        user_id = post.user_id,
        name = user.name,
        username = user.username,
        caption = post.caption,
        created_at = post.created_at,
        updated_at = post.updated_at
    )
    return post

