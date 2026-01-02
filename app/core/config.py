
from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    BASE_URL : str = config("BASE_URL", default = "http://localhost:5000")
    API_PREFIX : str = config("API_PREFIX", default = "/api/v2")
    PORT : int = config("PORT", default = 5000)
    DATABASE_URL: str = config("DATABASE_URL", default="postgresql://postgres:postgres@127.0.0.1:5432/backend_auto_system")

    class Config:
        env_file = ".env"