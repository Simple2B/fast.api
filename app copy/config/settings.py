from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SERVER_NAME: str = "FastAPI skeleton"
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    ENV: str = "production"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP: str = "3600"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    LOCAL_DB_PORT: str
    LOCAL_DB_SERVER: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        db_host = values["LOCAL_DB_SERVER"] if values["ENV"] == "develop" else values["POSTGRES_SERVER"]
        db_port = values["LOCAL_DB_PORT"] if values["ENV"] == "develop" else values["POSTGRES_PORT"]
        return PostgresDsn.build(
            scheme="postgres",
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=db_host,
            port=db_port,
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
