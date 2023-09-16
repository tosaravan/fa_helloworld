from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.dbutil import get_db


# Defining a Router
router = APIRouter(
    prefix="/it_comp",
    tags=["it_comp"]
)


@router.post('/', response_model=schemas.JobPostCreate)
def create_job_post(job: schemas.JobPostCreate, db: Session = Depends(get_db)):

    return crud.create_job_posts(db=db, job_post=job)

