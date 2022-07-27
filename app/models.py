# models.py allows communication between API and database
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"
    posts_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    posts_content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.users_id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    users_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    phone_number = Column(String)


class Votes(Base):
    __tablename__ = "votes"
    users_id = Column(
        Integer, ForeignKey("users.users_id", ondelete="CASCADE"), primary_key=True
    )
    posts_id = Column(
        Integer, ForeignKey("posts.posts_id", ondelete="CASCADE"), primary_key=True
    )
