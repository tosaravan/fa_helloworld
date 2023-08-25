from fastapi import APIRouter

# Defining a Router
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.get("/users/username", tags=["users"])
async def get_username(username: str):
    return {"username": username}


@router.get("/users",tags=["users"])
async def username(user_name: str, designation: str):
    return {"user_name": user_name, "designation": designation}


@router.get("/hello", tags=["users"])
async def hello(name:str,age:int):
   return {"name": name, "age":age}

@router.get("/hello/{name}/{age}")
async def hello(name,age):
   return {"name": name, "age":age}