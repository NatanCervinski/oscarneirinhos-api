from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from .db import init_db
from .routes import router

init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    print("Aplicação finalizando...")


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
