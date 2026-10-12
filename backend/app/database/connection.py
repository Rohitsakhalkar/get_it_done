from sqlalchemy import create_engine, event
from pathlib import Path
from sqlalchemy.orm import sessionmaker

path = Path(__file__).parent.parent.parent.parent
db_path = path/"database"/"get_it_done.db"
engine = create_engine(f"sqlite:///{db_path}")

SessionLocal = sessionmaker(engine)

@event.listens_for(engine,"connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


