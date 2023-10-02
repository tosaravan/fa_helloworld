from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dbutil import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customer"],
)


@router.post("/", response_model=schemas.CustomerBase)
def create_customer(Customer: schemas.CustomerBase, db: Session = Depends(get_db)):
    return crud.create_customer(customer_info=Customer, db=db)


@router.get("/", )
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_customers = crud.get_customers(db=db, skip=skip, limit=limit)

    return all_customers


@router.get("/id", )
def get_customer_id(customers_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_id(customer_id=customers_id, db=db)


@router.get("/email", )
def get_customer_email(customers_mail: str, db: Session = Depends(get_db)):
    return crud.get_customer_email(customer_email=customers_mail, db=db)


@router.get("/city", )
def get_customer_city(customer_city: str, db: Session = Depends(get_db)):
    return crud.get_customer_city(customer_city=customer_city, db=db)
