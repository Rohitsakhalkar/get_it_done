from app.security import verify_password, hash_password

password = "hello_123"

hashed_password =  hash_password(password)

print(verify_password(password, hashed_password))
print(verify_password("hello",hashed_password))