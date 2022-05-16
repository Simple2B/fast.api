from pydantic import BaseSettings


class Settings(BaseSettings):
    SAMPLE_ENV_VAR: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URI: str = ""
    DEV_DATABASE_URI: str

    class Config:
        env_file = ".env"


settings = Settings()
