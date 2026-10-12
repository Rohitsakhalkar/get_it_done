from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database.connection import SessionLocal

db = SessionLocal()

try:
    print("Foreign keys:", db.execute(text("PRAGMA foreign_keys")).scalar())

    db.execute(
        text("""
        INSERT INTO posts (user_id, caption)
        VALUES (-999, 'Foreign key test')
    """)
    )
    db.commit()
    print("Foreign key enforcement failed!")

except IntegrityError:
    db.rollback()   
    print("Foreign key enforcement works!")

finally:
    db.close()
