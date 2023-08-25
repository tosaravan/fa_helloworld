from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from .helper import *


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, firstname: str, lastname: str):
    return db.query(models.User).filter(and_(models.User.firstname == firstname, models.User.lastname == lastname)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(plain_text_password=user.password.encode("utf-8"))
    db_user = models.User(firstname=user.firstname,lastname=user.lastname,email=user.email,mobile=user.mobile,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
