from contextlib import asynccontextmanager

from fastapi import FastAPI

from image_search import api
from image_search.db import create_db_and_tables, get_or_create_engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    engine = get_or_create_engine()
    create_db_and_tables(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
