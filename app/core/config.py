from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    SECRET_KEY: str
    ENCRYPTION_KEY: Optional[str] = None
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/shieldvault"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    class Config:
        env_file = ".env"

settings = Settings()