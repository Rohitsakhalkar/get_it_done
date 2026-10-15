from app.security import hash_password, verify_password, create_access_token, decode_access_token
import pytest
from fastapi import HTTPException


def test_hash_password():
    password = "hello@123"
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password)
    assert hashed_password != password

def test_invalid_hash_password():
    password = "hello@123"
    hashed_password = hash_password(password)
    password2 = "Hello@123"
    assert not verify_password(password2, hashed_password) 

def test_token_creation():
    data = {
        "sub": str(1)
    }
    access_token = create_access_token(data)
    decode_data = decode_access_token(access_token)
    assert decode_data.get("sub") == data.get("sub")

def test_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        decode_access_token("j2e2gtTQ3RYP9uqirfo3qy8o73jqwekqih")
    assert exc_info.value.status_code == 401