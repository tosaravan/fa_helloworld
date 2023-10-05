from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dbutil import get_db

router = APIRouter(
    prefix="/chefs",
    tags=["Hotel Chefs"],
)


@router.post("/", response_model=schemas.ChefBase)
def create_chef(chef: schemas.ChefCreate, db: Session = Depends(get_db)):
    db_chef = crud.create_chef(chef_info=chef, db=db)

    chef_base = schemas.ChefBase(
        full_name=db_chef.full_name,
        speciality_cuisine=db_chef.speciality_cuisine,
        city=db_chef.city
    )

    return chef_base


@router.get('/', )
def get_chefs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_chefs = crud.get_chefs(db=db, skip=skip, limit=limit)

    return all_chefs


# @router.get('/{id}')
# def get_chef_id(chef_id: int, db: Session = Depends(get_db)):
#     return crud.get_chef_id(chef_id=chef_id, db=db)


@router.get("/{chef_id}")
def get_chef_by_id(chef_id: int , db: Session = Depends(get_db)):
    return crud.get_chef_id(chef_id=chef_id, db=db)


@router.get('/email')
def get_chef_email(chef_mail: str, db: Session = Depends(get_db)):
    return crud.get_chef_email(chef_mail=chef_mail, db=db)


@router.get('/city')
def get_chef_place(chef_city: str, db: Session = Depends(get_db)):
    return crud.get_chef_place(chef_place=chef_city, db=db)
