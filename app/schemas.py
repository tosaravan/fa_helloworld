from typing import List
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


class ShoppingItemRequest(BaseModel):
    product_name: str
    product_cost:  float
    total_units: int


class ShoppingCartRequest(BaseModel):
    customer_name: str
    items: List[ShoppingItemRequest]


class JobPostBase(BaseModel):
    job_reference: str
    job_details: str
    job_salary: float
    job_category: str


class JobPostCreate(JobPostBase):

    id: int
    is_active: bool

    class Config:
        orm_mode = True


