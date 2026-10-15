import os
import jwt
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from dotenv import load_dotenv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT/".env")
SECRET_KEY = os.environ["JWT_TOKEN"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()

def hash_password(password: str):
    db_password = password_hash.hash(password)
    return db_password

def verify_password(password: str , hashed_password: str):
    verify = password_hash.verify(password, hashed_password)
    return verify

def create_access_token(data: dict):
    copy_data = data.copy()
    copy_data["exp"] = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(copy_data, SECRET_KEY, algorithm = ALGORITHM)
    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code = 401 , detail = "Invalid token or token expired")