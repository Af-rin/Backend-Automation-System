from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    BASE_URL: str = "http://localhost:5000"
    API_PREFIX: str = "/api/v1"
    PORT: int = 5000

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@127.0.0.1:5432/backend_auto_system"

    # Auth
    REGISTRATION_TOKEN: str | None = None
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ENCRYPTION_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",   
        case_sensitive=False
    )


settings = Settings()
