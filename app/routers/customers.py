from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud, pydantic_models
from app.dbutil import get_db
from app.pydantic_models import CustomerBase

router = APIRouter(
    prefix="/customers",
    tags=["Customer"],
)


# @router.post("/", response_model=CustomerBase)
# def create_customer(Customer: CustomerBase, db: Session = Depends(get_db)):
#     return crud.create_customer(customer_info=Customer, db=db)

@router.post("/", response_model=CustomerBase)
def create_customer(customer: CustomerBase, db: Session = Depends(get_db)):
    db_customer = crud.create_customer(customer_info=customer, db=db)

    customer_base = CustomerBase(
        full_name=db_customer.full_name,
        city=db_customer.city,
        mobile=db_customer.mobile,
        email=db_customer.email
    )

    return customer_base


@router.get("/", )
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_customers = crud.get_customers(db=db, skip=skip, limit=limit)

    return all_customers


# @router.get("/{customer_id}")
# def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
#     return crud.get_customer_id(customer_id=customer_id, db=db)


@router.get("/email", )
def get_customer_email(customers_mail: str, db: Session = Depends(get_db)):
    return crud.get_customer_email(customer_email=customers_mail, db=db)


@router.get("/city", )
def get_customer_city(customer_city: str, db: Session = Depends(get_db)):
    return crud.get_customer_city(customer_city=customer_city, db=db)
