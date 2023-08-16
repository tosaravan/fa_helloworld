from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.dbutil import get_db

# Defining a Router
router = APIRouter(
    prefix="/usermgt",
    tags=["usermgt"],)


@router.get("/",)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@router.post('/', response_model=schemas.User, )
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return crud.create_user(db=db, user=user)
