import uvicorn
from fastapi import FastAPI, Path, Body, Request, Form
from typing import List
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Declaring the FastAPI as "app"
app = FastAPI()

# Declaring the Template Object
templates = Jinja2Templates(directory="templates")

# Parameter for mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# This is for the FAST Api Logo (Static Files)


@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name:str):
   return templates.TemplateResponse("hello.html", {"request": request, "name":name})


#  This is a templateResponse()
#  This is Hello World

@app.get("/hello/",response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


# This is with Name - Welcome (Templates Moved UP)
@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name:str):
   return templates.TemplateResponse("hello.html", {"request": request, "name":name})


# This is for the login template

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})

# This is for Submit
@app.post("/submit/")
async def submit(nm: str = Form(...), pwd: str = Form(...)):
   return {"username": nm}


# This is another alternative for submit function (using models)

class User(BaseModel):
   username:str
   password:str


@app.post("/submit/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
   return User(username=nm, password=pwd)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/hello/{name}/designation")

async def name_designation(name: str):

    # Name with Designation of the employee

    return {"Designation": f"{name} is working as Back-end API Developer"}


@app.get("/hello/{name}/{age}")
async def say_hello(name: str, age: int):
    return {"message": f"Hello {name} you are {age} years old"}

# This is the Query parameter
@app.get("/hello")
async def say_hello(name: str, age: int):
    return {"message": f"Hello {name} you are {age} years old"}


# This is the parameter validation
@app.get("/hello/{name}")
async def hello(name: str = Path(...,min_length=3,max_length=10)):
  return {"name": name}


# This is with the numeric parameters
@app.get("/hello/{name}/{age}")
async def hello(name: str = Path(...,min_length=3,max_length=10), age: int=Path(...,ge=1,le=100)):
    return {"name": name, "age": age}


# Model for Students
class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List[str] = []


# Request Body with POST
@app.post("/students/")
async def student_data(s1: Student):
   return s1


# Request Body with Body Class
@app.post("/students/")
async def student_data(name: str = Body(...), marks: int = Body(...)):
   return {"name": name, "marks": marks}


# Request Body with path parameter
@app.post("/students/{college}")
async def student_data(college: str, age: int, student: Student):
    retval = {"college": college, "age": age, **student.dict()}
    return retval



