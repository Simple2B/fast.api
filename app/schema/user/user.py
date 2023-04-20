from pydantic import BaseModel, EmailStr
from datetime import datetime


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    uuid: str
    created_at: datetime | str

    class Config:
        orm_mode = True
