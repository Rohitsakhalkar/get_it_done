from sqlalchemy import inspect
from app.database.connection import engine

inspector = inspect(engine)

print("Users columns:")
for column in inspector.get_columns("users"):
    print(column["name"], column["type"], "nullable:", column["nullable"])

print("\nUsers constraints:")
print(inspector.get_unique_constraints("users"))