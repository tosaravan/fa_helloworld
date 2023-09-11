from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.dbutil import get_db

# Defining a Router
router = APIRouter(
    prefix="/usermgt",
    tags=["usermgt"], )


@router.get("/", )
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@router.get("/email")
def get_user_email(email: str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db, email=email)


@router.get("/search")
def get_user_by_name(firstname: str, lastname: str, db: Session = Depends(get_db)):
    return crud.get_user_by_name(db, firstname=firstname, lastname=lastname)


@router.get("/users/username", tags=["users"])
async def get_username(username: str):
    return {"username": username}


@router.get("/users", tags=["users"])
async def username(user_name: str, designation: str):
    return {"user_name": user_name, "designation": designation}


@router.get("/hello", tags=["users"])
async def hello(name: str, age: int):
    return {"name": name, "age": age}


@router.get("/hello/{name}/{age}")
async def hello(name, age):
    return {"name": name, "age": age}


@router.post('/', response_model=schemas.User, )
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return crud.create_user(db=db, user=user)


@router.post('/cart', )
def create_shopping_cart(cart_usermgt: schemas.ShoppingCartRequest, db_usermgt: Session = Depends(get_db)):
    print(cart_usermgt.customer_name)
    for item in cart_usermgt.items:
        print("Product Name:", item.product_name)
        print("Product Cost:", item.product_cost)
        print("Total Units:", item.total_units)
        print("---")
    db_cart = crud.create_shopping_cart(db_usermgt, cart_usermgt)
    return f"cart_id: {db_cart.id}"


