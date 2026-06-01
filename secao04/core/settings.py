# from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "localhost"
    # SERVER_HOST: AnyHttpUrl = "http://localhost/8000"
    # BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str = "Curso FastAPI"
    PROJECT_VERSION: str = "0.1.0"
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./app.db"

    class Config:
        case_sensitive = True


settings = Settings()
