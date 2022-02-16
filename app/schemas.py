from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
