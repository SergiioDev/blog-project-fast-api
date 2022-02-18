from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    email: EmailStr


class UserLogin(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    owner: UserResponse

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    Post: PostBase
    likes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
