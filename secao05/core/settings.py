from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "localhost"
    # SERVER_HOST: AnyHttpUrl = "http://localhost/8000"
    # BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str = "Curso FastAPI - Seção 05 - Autenticação e Autorização"
    PROJECT_DESCRIPTION: str = (
        "API para gerenciamento de usuários e artigos com autenticação e autorização"
    )
    PROJECT_VERSION: str = "0.1.0"
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./app.db"

    JWT_SECRET_KEY: str = "TxMTgy0bKJBo3BmsXYOHLTV31r9K0Dipxzh9bkls43M"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True


settings = Settings()
