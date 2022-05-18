from pydantic import BaseSettings


class Settings(BaseSettings):
    SAMPLE_ENV_VAR: str = "<None>"
    JWT_SECRET: str = "<None>"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URI: str = ""
    DEV_DATABASE_URI: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()
