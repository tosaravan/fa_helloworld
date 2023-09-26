from fastapi import APIRouter, Path, Body, Request
from typing import List
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/tutorial_point",
    tags=["tutorial_point"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root():
    return {"message": "Hello World"}


# @router.get("/hello/{name}")
# async def hello(name):
#     return {"name": name}


@router.get("/hello/{name}/{age}")
async def hello(name, age):
    return {"name": name, "age": age}


@router.get("/hello/{name}/{age}")
async def hello(name: str, age: int):
    return {"name": name, "age": age}


# @router.get("/hello")
# async def hello(name: str, age: int):
#     return {"name": name, "age": age}


# @router.get("/hello/{name}")
# async def hello(name: str, age: int):
#     return {"name": name, "age": age}


@router.get("/hello/{name}")
async def hello(name: str = Path(..., min_length=3, max_length=10)):
    return {"name": name}


@router.get("/hello/{name}/{age}")
async def hello(*, name: str = Path(..., min_length=3, max_length=10), age: int = Path(..., ge=1, le=100)):
    return {"name": name, "age": age}


# class Student(BaseModel):
#     id: int
#     name: str = Field(None, title="Name of Student", max_length=10)
#     subjects: List[str] = []


# @router.post("/students/")
# async def student_data(s1: Student):
#     return s1
#

@router.post("/students")
async def student_data(name: str = Body(...), marks: int = Body(...)):
    return {"name": name, "marks": marks}


# @router.post("/students/{college}")
# async def student_data(college: str, age: int, student: Student):
#     retval = {"college": college, "age": age, **student.dict()}
#     return retval


# @router.get("/hello/")
# async def hello():
#    ret='''
# <html>
# <body>
# <h2>Hello World!</h2>
# </body>
# </html>
# '''
#    return HTMLResponse(content=ret)


@router.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


# Students Model
class Student(BaseModel):
    id: int
    name: str = Field(None, title="name of student", max_length=10)
    English: int
    Maths: int


# Percent Model (Response Model)
class Percent(BaseModel):
    id: int
    name: str = Field(None, title="name of student", max_length=10)
    percent_marks: float
    average_mark: float
    total_marks: int


# Response Model - Percentage of Students
@router.post("/marks", response_model=Percent)
async def get_percent(s1: Student):
    total_marks = s1.Maths + s1.English
    average_marks = total_marks / 2
    percentage = (average_marks / 100) * 100

    marks = Percent(
        id=s1.id,
        name=s1.name,
        percent_marks=percentage,
        total_marks=total_marks,
        average_mark=average_marks,
    )

    return marks
