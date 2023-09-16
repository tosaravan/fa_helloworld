from http.client import HTTPException

from fastapi import APIRouter
from fastapi import Depends
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


@router.get("/", )
def get_job_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_posts = crud.get_job_posts(db, skip=skip, limit=limit)
    return job_posts


@router.get("/id")
def get_job_posts_id(post_id: int, db: Session = Depends(get_db)):
    return crud.get_job_posts_id(db, post_id=post_id)

