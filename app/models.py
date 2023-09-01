from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import deferred, relationship
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


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)

    items = relationship("ShoppingItems", back_populates="cart")


class ShoppingItems(Base):
    __tablename__ = "shopping_items"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, unique=True, index=True)
    product_cost = Column(Float)
    total_units = Column(Integer)
    cart_id = Column(Integer, ForeignKey(ShoppingCart.id))

    cart = relationship("ShoppingCart", back_populates="items")


