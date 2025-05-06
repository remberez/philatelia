import enum

from sqlalchemy import BigInteger, String, Boolean, Date, ForeignKey, Enum, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class UserRoles(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles))
    hashed_pass: Mapped[str] = mapped_column(String)

    collections: Mapped[List["Collection"]] = relationship(back_populates="owner")
    stamps: Mapped[List["Stamp"]] = relationship(back_populates="owner")
    groups: Mapped[List["Group"]] = relationship(secondary="user_group", back_populates="users")
    meetings: Mapped[List["Meeting"]] = relationship(secondary="meeting_user", back_populates="visitors")
    user_groups: Mapped[List["Group"]] = relationship(back_populates="group_owner")

class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    groupname: Mapped[str] = mapped_column(String, unique=True, index=True)
    group_owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))

    group_owner: Mapped["User"] = relationship(back_populates="user_groups")
    posts: Mapped[List["Post"]] = relationship(back_populates="group")
    meetings: Mapped[List["Meeting"]] = relationship(back_populates="group")
    post_photos: Mapped[List["PostPhoto"]] = relationship(back_populates="group")
    users: Mapped[List["User"]] = relationship(secondary="user_group", back_populates="groups")

class UserGroup(Base):
    __tablename__ = "user_group"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), primary_key=True, index=True)

class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    group: Mapped["Group"] = relationship(back_populates="posts")

class PostPhoto(Base):
    __tablename__ = "post_photo"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    photo_url: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)

    group: Mapped["Group"] = relationship(back_populates="post_photos")

class Meeting(Base):
    __tablename__ = "meeting"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
    photo_url: Mapped[str] = mapped_column(String)

    group: Mapped["Group"] = relationship(back_populates="meetings")
    visitors: Mapped[List["User"]] = relationship(secondary="meeting_user", back_populates="meetings")

class MeetingUser(Base):
    __tablename__ = "meeting_user"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, index=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), primary_key=True, index=True)
    is_visited: Mapped[bool] = mapped_column(Boolean)

class Stamp(Base):
    __tablename__ = "stamp"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country: Mapped[int] = mapped_column(BigInteger, index=True)
    issue_year: Mapped[Date] = mapped_column(Date, index=True)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    owner: Mapped["User"] = relationship(back_populates="stamps")
    collections: Mapped[List["Collection"]] = relationship(secondary="stamp_collection", back_populates="stamps")

class Collection(Base):
    __tablename__ = "collection"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    owner: Mapped["User"] = relationship(back_populates="collections")
    stamps: Mapped[List["Stamp"]] = relationship(secondary="stamp_collection", back_populates="collections")

class StampCollection(Base):
    __tablename__ = "stamp_collection"

    stamp_id: Mapped[int] = mapped_column(ForeignKey("stamp.id"), primary_key=True, index=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"), primary_key=True, index=True)


db_url = "postgresql+asyncpg://user:password@localhost:5433/filatel"


engine = create_async_engine(db_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
