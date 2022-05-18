from pydantic import BaseModel
from datetime import datetime
from .user_out import UserOut


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user: UserOut

    class Config:
        orm_mode = True
