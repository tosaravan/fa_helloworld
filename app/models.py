from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import deferred
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=True, index=True)
    lastname = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    hashed_password = deferred(Column(String))
    is_active = Column(Boolean, default=True)