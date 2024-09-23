from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import ClassVar
from sqlalchemy.orm.decl_api import DeclarativeMeta


class Settings(BaseSettings):
    DB_URL: str = config("DB_URL")
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()
    TEMPLATES: ClassVar[Jinja2Templates] = Jinja2Templates(directory="templates")
    MEDIA: ClassVar[Path] = Path('media')

    class Config:
        case_sensitive = True


settings: Settings = Settings()