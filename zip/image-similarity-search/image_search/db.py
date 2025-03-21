from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import SQLModel, Field, create_engine, Session

from image_search.settings import get_settings


class Image(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid4()), max_length=32, primary_key=True)
    filename: str
    # TODO: we should probably store the features in a separate table
    features: bytes


_engine: Engine | None = None


def get_or_create_engine() -> Engine:
    global _engine
    if _engine is None:
        settings = get_settings()
        connect_args = {"check_same_thread": False}
        _engine = create_engine(settings.sqlite_url, connect_args=connect_args)
    return _engine


def create_db_and_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(get_or_create_engine()) as session:
        yield session


DatabaseSessionDep = Annotated[Session, Depends(get_session)]
