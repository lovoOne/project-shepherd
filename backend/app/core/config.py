from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Project Shepherd API"
    VERSION: str = "0.1.0"

    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()