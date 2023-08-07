import uvicorn
import shutil
from fastapi import FastAPI, Path, Body, Request, Form, File, UploadFile, Cookie, Header, Depends
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field, constr
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


# Declaring the FastAPI as "app"
app = FastAPI()

# Declaring the Template Object
templates = Jinja2Templates(directory="templates")

# Parameter for mount
app.mount("/static", StaticFiles(directory="static"), name="static")


# This is for the FAST Api Logo (Static Files)


@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name: str):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})


#  This is a templateResponse()
#  This is Hello World

@app.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request})


# This is with Name - Welcome (Templates Moved UP)
@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name: str):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})


# This is for the login template

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# This is for Submit
@app.post("/submit-v1/")
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return {"username": nm}


# This is another alternative for submit function (using models)

class User(BaseModel):
    username: str
    password: str


@app.post("/submit-v2/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return User(username=nm, password=pwd)


# Uploading files

@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   return templates.TemplateResponse("uploadfile.html", {"request": request})


# Uploader Operation

async def create_upload_file(file: UploadFile = File(...)):
   with open("destination.png", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   return {"filename": file.filename}


# Cookie Parameter - (set cookie method)
# Create Cookie
@app.post("/cookie/")
def create_cookie():
   content = {"message": "cookie set"}
   response = JSONResponse(content=content)
   response.set_cookie(key="username", value="admin")
   return response


# To read the Cookie

@app.get("/readcookie/")
async def read_cookie(username: str = Cookie(None)):
   return {"username": username}


# This is the Header Parameter
@app.get("/headers/")
async def read_header(accept_language: Optional[str] = Header(None)):
   return {"Accept-Language": accept_language}


# This is Response Type Header
@app.get("/rspheader/")
def set_rsp_headers():
   content = {"message": "Hello World"}
   headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
   return JSONResponse(content=content, headers=headers)


# Response Model Parameter


# Students Model
class student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   marks: List[int] = []
   percent_marks: float


# Precent Model (Response Model)
class percent(BaseModel):
   id:int
   name :str = Field(None, title="name of student", max_length=10)
   percent_marks: float


# Response Model - Percentage of Students
@app.post("/marks", response_model=percent)
async def get_percent(s1:student):
   s1.percent_marks=sum(s1.marks)/2
   return s1


# Response Model

# Model for Supplier
class supplier(BaseModel):
   supplierID:int
   supplierName:str


# Model for Product
class product(BaseModel):
   productID:int
   prodname:str
   price:int
   supp:supplier


# Model for  customer
class customer(BaseModel):
   custID:int
   custname:str
   prod:Tuple[product]


# To generate the invoice

@app.post('/invoice')
async def getInvoice(c1:customer):
   return c1


#  Pydantic Model for Class

data = []
class Book1(BaseModel):
   id: int
   title: str
   author: str
   publisher: str


# This is function to create add a book
@app.post("/book")
def add_book(book: Book1):
   data.append(book.dict())
   return data


# To Retrieve the data of the added books
@app.get("/list")
def get_books():
   return data


# To Retrieve the books with the ID Parameter

@app.get("/book/{id}")
def get_book(id: int):
   id = id - 1
   return data[id]


# PUT decorator that modifies an object in the data list with the ID parameter

@app.put("/book/{id}")
def add_book(id: int, book: Book1):
   data[id-1] = book
   return data


# DELETE decorater to delete an object with ID parameter

@app.delete("/book/{id}")
def delete_book(id: int):
   data.pop(id-1)
   return data


# SQL Database
# Creating a database engine for our database called test.db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})


# Session object (handle) to obtain the Database.

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for storing the Classes and the mapped tables.

Base = declarative_base()


# Creating the table

class Books(Base):
   __tablename__ = 'book'
   id = Column(Integer, primary_key=True, nullable=False)
   title = Column(String(50), unique=True)
   author = Column(String(50))
   publisher = Column(String(50))
   Base.metadata.create_all(bind=engine)
# create_all() method creates the corresponding tables in the database


# Pydantic model that corresponds to the declarative base

class Book(BaseModel):
   id: int
   title: str
   author:str
   publisher: str
   class Config:
      orm_mode = True

# CRUD operations with the database through SQL alchemy

def get_db():
   db = session()
   try:
      yield db
   finally:
    db.close()

# To Add a Book

@app.post('/add_new', response_model=Book)
def add_book(b1: Book, db: Session = Depends(get_db)):
   bk=Books(id=b1.id, title=b1.title, author=b1.author, publisher=b1.publisher)
   db.add(bk)
   db.commit()
   db.refresh(bk)
   return Books(**b1.dict())


# To get all the records of the book

@app.get('/list', response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
   recs = db.query(Books).all()
   return recs


# With the path parameter

@app.get('/book/{id}', response_model=Book)
def get_book(id:int, db: Session = Depends(get_db)):
   return db.query(Books).filter(Books.id == id).first()


# To Update the book records

@app.put('/update/{id}', response_model=Book)
def update_book(id:int, book:Book, db: Session = Depends(get_db)):
   b1 = db.query(Books).filter(Books.id == id).first()
   b1.id=book.id
   b1.title=book.title
   b1.author=book.author
   b1.publisher=book.publisher
   db.commit()
   return db.query(Books).filter(Books.id == id).first()


# To delete the book
@app.delete('/delete/{id}')
def del_book(id:int, db: Session = Depends(get_db)):
   try:
      db.query(Books).filter(Books.id == id).delete()
      db.commit()
   except Exception as e:
      raise Exception(e)
   return {"delete status": "success"}

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
async def hello(name: str = Path(..., min_length=3, max_length=10)):
    return {"name": name}


# This is with the numeric parameters
@app.get("/hello/{name}/{age}")
async def hello(name: str = Path(..., min_length=3, max_length=10), age: int = Path(..., ge=1, le=100)):
    return {"name": name, "age": age}



