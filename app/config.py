import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    secret_key: str = os.getenv("SECRET_KEY", "supersecret")
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"

settings = Settings()
