from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True