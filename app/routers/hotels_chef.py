from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud, pydantic_models, db_models
from app.dbutil import get_db

router = APIRouter(
    prefix="/chefs",
    tags=["Hotel Chefs"],
)


@router.post("/", response_model=pydantic_models.ChefBase)
def create_chef(chef: pydantic_models.ChefCreate, db: Session = Depends(get_db)):
    db_chef = crud.create_chef(chef_info=chef, db=db)

    chef_base = pydantic_models.ChefBase(
        full_name=db_chef.full_name,
        speciality_cuisine=db_chef.speciality_cuisine,
        city=db_chef.city
    )

    return chef_base


@router.get('/', )
def get_chefs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_chefs = crud.get_chefs(db=db, skip=skip, limit=limit)

    return all_chefs


@router.get("/id")
def get_chef_by_id(chef_id: int, db: Session = Depends(get_db)):
    return crud.get_chef_id(chef_id=chef_id, db=db)


@router.get('/email')
def get_chef_email(chef_mail: str, db: Session = Depends(get_db)):
    return crud.get_chef_email(chef_mail=chef_mail, db=db)


@router.get('/city')
def get_chef_place(chef_city: str, db: Session = Depends(get_db)):
    return crud.get_chef_place(chef_place=chef_city, db=db)


@router.post("/{chef_id}/customers/{customer_id}")
def link_customer_with_chef(chef_id: int, customer_id: int, link_data: pydantic_models.LinkCustomerWithChefInput, db: Session = Depends(get_db)):

    # Verify if the chef exists
    chef = crud.get_chefs(db, chef_id)
    if not chef:
        raise HTTPException(status_code=404, detail="Chef not found")

    # Verify if the customer exists
    customer = crud.get_customers(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    link = crud.create_chef_customer_link(db, chef_id, customer_id, link_data.description)

    return {
        "chefId": link.chef_id,
        "customerId": link.customer_id,
        "description": link.description,
        "status": "Customer linked with Chef",
    }


@router.get("/{chef_id}/customer",)
def get_customer_for_chef(chef_id: int, db: Session = Depends(get_db)):
    customers = crud.get_customer_for_chef(chef_id=chef_id, db=db)
    return customers



