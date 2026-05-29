from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./app.db"
    BASE_MODEL = declarative_base()

    class Config:
        case_sensitive = True