from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from ..dependencies import get_token_header
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import List
from pydantic import BaseModel, constr

# Creating a database engine for User usermgt.tb

SQLALCHEMY_DATABASE_URL = "sqlite:///./usermgt.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

# Session object (handle) to obtain the Database
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base to store the classes
Base = declarative_base()

usermgt = APIRouter(
    prefix="/usermgt",
    tags=["usermgt"],
    dependencies=[Depends(get_token_header)],
    responses={404:{"description": "Not Found"}},
)


# User Model
class Users(Base):
    userid: Column(Integer, primary_key=True, nullable=False)
    firstname: Column(String(100))
    lastname: Column(String(50))
    email: Column(String(50), unique=True)
    mobile: Column(String(50), unique=True)
# Create_all() method creates the corresponding tables in the database
    Base.metadata.create_all(bind=engine)


# Pydantic Model for the User Class

class User(BaseModel):
    userid: int
    firstname: str
    lastname: str
    email: str
    mobile: str

    class Config:
        orm_mode = True


Base.metadata.create_all(bind=engine)

def get_db():
   db = session()
   try:
      yield db
   finally:
       db.close()


# To add Users
@usermgt.post("/add_user", response_model=User)
def add_user(u1: User, db: Session = Depends(get_db):
    um = Users(userid=u1.userid, firstname=u1.firstname, lastname=u1.lastname, email=u1.email, mobile=u1.mobile)
    db.add(um)
    db.commit()
    db.refresh(um)
    return Users(**u1.dict())


#  To get all the users list

@usermgt.get("/list", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    user_rec = db.query(Users).all()
    return user_rec


# To get the users with the ID
@usermgt.get("/user/{id}", response_model=User)
def get_user(id:int, db: Session = Depends(get_db)):
    return db.query(Users).filter(Users.userid==id).first()