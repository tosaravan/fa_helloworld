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
    product_cost: float
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


# Response Model ( Chef's FullName , Speciality Cuisine and City)
class ChefBase(BaseModel):
    full_name: str
    speciality_cuisine: str
    city: str


# To Create Chef's
class ChefCreate(ChefBase):
    mobile: str
    email: str
    id: int


class CustomerBase(BaseModel):
    full_name: str
    city: str
    mobile: str
    email: str


class CustomerCreate(CustomerBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class CustomerWithChefLink(BaseModel):
    id: int
    full_name: str
    mobile: str
    email: str
    description: str

    class Config:
        orm_mode = True
