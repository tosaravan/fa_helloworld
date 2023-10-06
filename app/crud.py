from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import db_models, pydantic_models
from .helper import *
from .db_models import ShoppingItem


def get_user(db: Session, user_id: int):
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()


def get_user_by_name(db: Session, firstname: str, lastname: str):
    return db.query(db_models.User).filter(
        and_(db_models.User.firstname == firstname, db_models.User.lastname == lastname)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: pydantic_models.UserCreate):
    hashed_password = get_hashed_password(plain_text_password=user.password.encode("utf-8"))
    db_user = db_models.User(firstname=user.firstname, lastname=user.lastname, email=user.email, mobile=user.mobile,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_shopping_cart(db: Session, shopping_cart: pydantic_models.ShoppingCartRequest):
    # shopping_items = [x for x in shopping_cart.items] TODO should use composition rather iteration as below
    shopping_items: List = []
    for item in shopping_cart.items:
        item = ShoppingItem(product_name=item.product_name, product_cost=item.product_cost, total_units=item.total_units)
        shopping_items.append(item)

    db_cart = db_models.ShoppingCart(customer_name=shopping_cart.customer_name, items=shopping_items)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


def create_job_posts(db: Session, job_post: pydantic_models.JobPostCreate):
    db_jobs = db_models.JobPosts(job_reference=job_post.job_reference, job_details=job_post.job_details, job_salary=job_post.job_salary, job_category=job_post.job_category)

    db.add(db_jobs)
    db.commit()
    db.refresh(db_jobs)

    return db_jobs


def get_job_posts_id(db: Session, post_id: int):
    return db.query(db_models.JobPosts).filter(db_models.JobPosts.id == post_id).first()


def get_job_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.JobPosts).offset(skip).limit(limit).all()


def get_job_post_cate(db: Session, job_category: str):
    return db.query(db_models.JobPosts).filter(db_models.JobPosts.job_category == job_category).first()


def create_chef(db: Session, chef_info: pydantic_models.ChefCreate):
    db_chef = db_models.Chef(full_name=chef_info.full_name, speciality_cuisine=chef_info.speciality_cuisine, city=chef_info.city, mobile=chef_info.mobile, email=chef_info.email )

    db.add(db_chef)
    db.commit()
    db.refresh(db_chef)

    return db_chef


def get_chefs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Chef).offset(skip).limit(limit).all()


def get_chef_id(db: Session, chef_id: int):
    return db.query(db_models.Chef).filter(db_models.Chef.id == chef_id).first()


def get_chef_email(db: Session, chef_mail: str):
    return db.query(db_models.Chef).filter(db_models.Chef.email == chef_mail).first()


def get_chef_place(db: Session, chef_place: str):
    return db.query(db_models.Chef).filter(db_models.Chef.city == chef_place).all()


def create_customer(db: Session, customer_info: pydantic_models.CustomerBase):
    db_customer = db_models.Customer(full_name=customer_info.full_name, city=customer_info.city, mobile=customer_info.mobile, email=customer_info.email)

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Customer).offset(skip).limit(limit).all()


def get_customer_id(db: Session, customer_id: int):
    return db.query(db_models.Customer).filter(db_models.Customer.id == customer_id).first()


def get_customer_email(db: Session, customer_email: str):
    return db.query(db_models.Customer).filter(db_models.Customer.email == customer_email).first()


def get_customer_city(db: Session, customer_city: str):
    return db.query(db_models.Customer).filter(db_models.Customer.city == customer_city).first()

