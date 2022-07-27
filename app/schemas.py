# schemas.py allows communication between client and API
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    posts_content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# define Response schema for /users
class UserOut(BaseModel):
    users_id: int
    email: EmailStr
    created_at = datetime

    class Config:
        orm_mode = True


# define Response schema for post
class Post(PostBase):
    posts_id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    post: Post = Field(..., alias="Post")
    votes: int = Field(..., alias="number of votes")

    class Config:
        orm_mode = True


# define Request schema for User Create
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    posts_id: int
    votes_dir: conint(le=1)
