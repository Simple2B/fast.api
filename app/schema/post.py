from pydantic import BaseModel
from datetime import datetime
from .user import User


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BasePost):
    id: int
    uuid: str
    created_at: datetime
    user: User

    class Config:
        orm_mode = True


class PostList(BaseModel):
    posts: list[Post]
