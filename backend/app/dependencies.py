from app.security import decode_access_token
from app.database.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from app.database.connection import get_db
from sqlalchemy.orm import Session

bearer = HTTPBearer()

def get_current_user(db: Session = Depends(get_db) , credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    payload = decode_access_token(credentials.credentials)
    user_data = payload.get("sub")
    if isinstance(user_data,str) and user_data.isdigit() and int(user_data) > 0:
        user_data = int(user_data)
    else: 
        raise HTTPException(status_code = 401, detail = "Invalid authentication Credentials")
    user = db.query(User).filter(User.id == user_data).first()
    if user:
        return user
    else:
        raise HTTPException(status_code = 401 , detail = "Unauthorized user")