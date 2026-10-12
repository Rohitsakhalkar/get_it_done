from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint, DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    username: Mapped[str] = mapped_column(unique = True, nullable = False)
    email: Mapped[str] = mapped_column(unique = True, nullable = False)
    password_hash: Mapped[str] = mapped_column(nullable = False) 
    work_location: Mapped[str | None] = mapped_column()
    home_location: Mapped[str | None] = mapped_column()
    bio: Mapped[str | None] = mapped_column()
    gender: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now(), onupdate = func.now())

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False)
    caption: Mapped[str] = mapped_column(nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now(), onupdate = func.now())

class Capabilities(Base):
    __tablename__ = "capabilities"
    __table_args__ = (UniqueConstraint("user_id" ,"capability", name = "uq_user_capabilties"),)
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable = False)
    capability: Mapped[str] = mapped_column(nullable = False)