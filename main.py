import uvicorn
import shutil
from fastapi import FastAPI, Path, Body, Request, Form, File, UploadFile, Cookie, Header
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse
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



