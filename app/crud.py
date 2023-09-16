from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from .helper import *
from .models import ShoppingItem


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, firstname: str, lastname: str):
    return db.query(models.User).filter(
        and_(models.User.firstname == firstname, models.User.lastname == lastname)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(plain_text_password=user.password.encode("utf-8"))
    db_user = models.User(firstname=user.firstname, lastname=user.lastname, email=user.email, mobile=user.mobile,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_shopping_cart(db: Session, shopping_cart: schemas.ShoppingCartRequest):
    # shopping_items = [x for x in shopping_cart.items] TODO should use composition rather iteration as below
    shopping_items: List = []
    for item in shopping_cart.items:
        item = ShoppingItem(product_name=item.product_name, product_cost=item.product_cost, total_units=item.total_units)
        shopping_items.append(item)

    db_cart = models.ShoppingCart(customer_name=shopping_cart.customer_name, items=shopping_items)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


def create_job_posts(db: Session, job_post: schemas.JobPostCreate):
    db_jobs = models.JobPosts(job_reference=job_post.job_reference, job_details=job_post.job_details, job_salary=job_post.job_salary, job_category=job_post.job_category)

    db.add(db_jobs)
    db.commit()
    db.refresh(db_jobs)

    return db_jobs


def get_job_posts_id(db: Session, post_id: int):
    return db.query(models.JobPosts).filter(models.JobPosts.id == post_id).first()


def get_job_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobPosts).offset(skip).limit(limit).all()

