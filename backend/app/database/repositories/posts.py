from app.database.models import Post, User
from app.schemas.posts import CreatePosts, ShowPosts, UpdatePost
from fastapi import HTTPException


def create_post(db, post: CreatePosts, current_user):
    
    db_post = Post(
        user_id = current_user.id,
        caption = post.caption
    )
    db.add(db_post)
    db.commit()
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
    db.commit()
    return "deleted"

def post_update(post_id, update_data: UpdatePost, db, current_user):
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code = 404 , detail = "Error post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code = 403 ,detail = "you don't have the permission to update this post")
    post.caption = update_data.caption
    db.commit() 
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

