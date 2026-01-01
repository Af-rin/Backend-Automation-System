
from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    BASE_URL : str = config("BASE_URL", default = "http://localhost:5000")
    API_PREFIX : str = config("API_PREFIX", default = "/api/v2")
    PORT : int = config("PORT", default = 5000)

    class Config:
        env_file = ".env"