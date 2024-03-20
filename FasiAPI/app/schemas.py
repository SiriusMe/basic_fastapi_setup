from pydantic import config, EmailStr, BaseModel
from datetime import datetime
from typing import Optional, List


# pydantic models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class GetPost(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class config:
        orm_mode = True


class PostList(BaseModel):
    posts: List[GetPost]


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
