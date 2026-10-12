from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from app.schemas.users import UserCreate
from sqlalchemy.orm import  Session
from app.database.connection import get_db

from app.database.repositories.users import create_user

from app.schemas.posts import CreatePosts, ShowPosts, UpdatePost
from app.database.repositories.posts import show_posts, post_update, post_delete, create_post


from app.schemas.capabilities import CreateCapabilities
from app.database.repositories.capabilities import create_capability,show_user_capabilities

app = FastAPI()

@app.post("/users")
def create_users(user: UserCreate,db: Session = Depends(get_db)):
    return create_user(db,user)
    

@app.post("/posts")
def create_posts(posts: CreatePosts, db: Session = Depends(get_db)):
    return create_post(db, posts)

@app.get("/posts",response_model=list[ShowPosts])
def show_post(db: Session = Depends(get_db), limit: int = Query(default = 10, ge = 1, le = 100),offset: int = Query(default = 0, ge = 0) ):
    return show_posts(db, limit, offset)

@app.delete("/posts/{post_id}")
def post_deletes(post_id: int ,db: Session = Depends(get_db)):
    return post_delete(db,post_id)

@app.patch("/posts/{post_id}")
def post_updates(post_id,update_post: UpdatePost,db: Session = Depends(get_db)):
    return post_update(post_id,update_post,db)

@app.post("/users/{user_id}/capabilities")
def create_capabilities(user_id, Create_Capability: CreateCapabilities ,db: Session = Depends(get_db)):
    try:
        return create_capability(user_id, Create_Capability,db)
    except IntegrityError:
        raise HTTPException(status_code = 409 , detail = "capability already exist. please add a new capability")

@app.get("/users/{user_id}/capabilities")
def show_capabilities(user_id, db: Session = Depends(get_db)):
    return show_user_capabilities(user_id,db)