from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    db_password = password_hash.hash(password)
    return db_password

def verify_password(password: str , hashed_password: str):
    verify = password_hash.verify(password, hashed_password)
    return verify