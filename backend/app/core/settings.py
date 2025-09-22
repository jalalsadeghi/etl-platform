# core/settings.py

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "etl_db"
    POSTGRES_USER: str = "etl_user"
    POSTGRES_PASSWORD: str = "etlPassword123!"

    secret_key: str = Field(
        ...,
        validation_alias=AliasChoices("SECRET_KEY", "secret_key"),
    )
    ALLOWED_ORIGINS: str = "*"

    ETL_SOURCE_URL: str = "https://jsonplaceholder.typicode.com/users"
    ETL_API_KEY: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file="backend/.env.development",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    server_name: str | None = Field(
        default=None, validation_alias=AliasChoices("SERVER_NAME", "server_name")
    )


settings = Settings()
