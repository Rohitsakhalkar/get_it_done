from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint, DateTime, func, CheckConstraint, Index
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

class Follows(Base):
    __tablename__ = "follows"
    __table_args__ = (UniqueConstraint("followed_by","followed_to",name = "uq_follows_followed_by_followed_to"),
                      CheckConstraint("followed_by != followed_to",name = "ck_follows_no_self_follow"),
                       Index("ix_follows_followed_to", "followed_to"))
    
    id: Mapped[int] = mapped_column(primary_key = True)
    followed_by: Mapped[int] = mapped_column(ForeignKey("users.id" , ondelete = "CASCADE"), nullable = False)
    followed_to: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now(), nullable = False)

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"),nullable = False)
    title: Mapped[str] = mapped_column(nullable = False)
    description: Mapped[str] = mapped_column(nullable = False)
    location: Mapped[str] = mapped_column()
    payment: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default = "open")
    cancellation_reason: Mapped[str | None] = mapped_column(nullable = True)
    cancelled_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"),nullable = True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now(), nullable = False) 
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now(), onupdate = func.now(), nullable = False)
 