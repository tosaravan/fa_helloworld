from fastapi import Depends, FastAPI

from . import models
from .database import engine
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users, usermgt, it_comp, tutorialspoint, hotels_chef

print("1")
models.Base.metadata.create_all(bind=engine)


print("2")

# if you need auth
# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(hotels_chef.router)
app.include_router(tutorialspoint.router)
app.include_router(it_comp.router)
app.include_router(usermgt.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
