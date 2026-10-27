from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import  Session
from app.database.connection import get_db

from app.database.models import User
from app.dependencies import get_current_user

from app.database.repositories.users import create_user, user_login, update_user_data, search_users, search_user
from app.schemas.users import UserCreate, UserLogin, UpdateUser

from app.schemas.posts import CreatePosts, ShowPosts, UpdatePost
from app.database.repositories.posts import show_posts, post_update, post_delete, create_post, get_post, get_user_post


from app.schemas.capabilities import CreateCapabilities, UpdateUserCapability
from app.database.repositories.capabilities import create_capability,show_user_capabilities, delete_capability, update_capability

from app.database.repositories.follows import follow_user, unfollow_user, get_follower_count, get_followers, get_following_count ,get_followings

app = FastAPI()

@app.post("/login")
def login(user: UserLogin, 
          db: Session = Depends(get_db) ):
    return user_login(db,user)

@app.get("/users/{username}")
def get_users(username: str,
              db: Session = Depends(get_db)):
    return search_user(username,db)

@app.get("/users")
def get_users(identifier: str = Query(min_length = 1),
               db: Session = Depends(get_db), 
              limit : int = Query(default = 10 , ge = 1, le = 100),
              offset: int = Query(default = 0, ge = 0)):
    return search_users(identifier, db, limit, offset)

@app.post("/signup", status_code = 201)
def create_users(user: UserCreate,
                 db: Session = Depends(get_db)):
    create_user(db,user)

@app.patch("/users/me")
def update_user(user: UpdateUser, 
                db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):
    return update_user_data(user, db, current_user)
    
@app.post("/posts")
def create_posts(posts: CreatePosts, 
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return create_post(db, posts, current_user)

@app.get("/posts",response_model=list[ShowPosts])
def show_feed(db: Session = Depends(get_db), 
              limit: int = Query(default = 10, ge = 1, le = 100),
              offset: int = Query(default = 0, ge = 0) ):
    return show_posts(db, limit, offset)

@app.get("/posts/{post_id}")
def show_post(post_id: int, db: Session = Depends(get_db)):
    return get_post(post_id, db)

@app.get("/users/{username}/posts",response_model = list[ShowPosts] )
def show_user_posts(username: str, 
                    db: Session = Depends(get_db), 
                    limit: int = Query(default = 10, ge = 1, le = 100), 
                    offset: int = Query(default = 0, ge = 0)):
    return get_user_post(username, db, limit, offset)

@app.delete("/posts/{post_id}", status_code = 204)
def post_deletes(post_id: int ,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    post_delete(db, post_id, current_user)

@app.patch("/posts/{post_id}")
def post_updates(post_id,update_post: UpdatePost,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_update(post_id, update_post, db, current_user)

@app.post("/users/capabilities")
def create_capabilities(Create_Capability: CreateCapabilities ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_capability(Create_Capability, db, current_user)
    except IntegrityError:
        raise HTTPException(status_code = 409 , detail = "capability already exist. please add a new capability")

@app.get("/users/{user_id}/capabilities")
def show_capabilities(user_id: int, db: Session = Depends(get_db)):
    return show_user_capabilities(user_id, db)

@app.delete("/users/capabilities/{capability_id}", status_code = 204)
def delete_capabilties(capability_id: int ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_capability(capability_id, db, current_user)

@app.patch("/users/capabilities/{capability_id}")
def update_capabilities(capability_id: int, update_data: UpdateUserCapability,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_capability(capability_id, update_data, db, current_user)

@app.post("/users/{username}/follow")
def follow(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return follow_user(username, db, current_user)

@app.delete("/users/{username}/follow", status_code = 204 )
def unfollow(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    unfollow_user(username,db,current_user)


@app.get("/users/{username}/followers/count")
def get_follower_count_route(username: str, db: Session = Depends(get_db)):
    return get_follower_count(username, db)

@app.get("/users/{username}/followings/count")
def get_following_count_route(username: str, db: Session = Depends(get_db)):
    return get_following_count(username,db)

@app.get("/users/{username}/followers")
def get_followers_route(username: str,
                         db: Session = Depends(get_db),
                         limit: int = Query(default = 10 , le = 100, ge = 1),
                        offset: int = Query(default = 0, ge = 0) ):
    return get_followers(username,db,limit,offset)

@app.get("/users/{username}/followings")
def get_following_route(username: str, 
                        db: Session = Depends(get_db),
                        limit: int = Query(default = 10 , le = 100, ge = 1),
                        offset: int = Query(default = 0, ge = 0)):
    return get_followings(username, db,limit,offset)