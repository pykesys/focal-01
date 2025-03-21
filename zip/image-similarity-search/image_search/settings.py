from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='image_search_')

    # TODO convert all paths and dirs to Path
    image_dir: str
    sqlite_url: str


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
