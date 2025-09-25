# backend/app/core/settings.py
import os

from dotenv import load_dotenv
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1) Load env file dynamically by APP_ENV
APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
env_path = f"backend/.env.{APP_ENV}"
load_dotenv(env_path, override=True)


class Settings(BaseSettings):
    # --- App ---
    APP_ENV: str = APP_ENV
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # --- DB ---
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "etl_db"
    POSTGRES_USER: str = "etl_user"
    POSTGRES_PASSWORD: str = "etlPassword123!"

    # --- Secrets ---
    secret_key: str = Field(
        ...,
        validation_alias=AliasChoices("SECRET_KEY", "secret_key"),
        description="Required; do not hardcode.",
    )
    API_KEY: str = Field(
        ...,
        validation_alias=AliasChoices("API_KEY", "api_key"),
        description="Required; used for simple API-key auth.",
    )

    ALLOWED_ORIGINS: str = "*"

    # --- ETL source ---
    ETL_SOURCE_URL: str = "https://jsonplaceholder.typicode.com/users"
    ETL_API_KEY: str | None = None

    # --- Domain (for nginx) ---
    server_name: str | None = Field(
        default=None, validation_alias=AliasChoices("SERVER_NAME", "server_name")
    )

    # --- Redis (rate-limit / tasks) ---
    REDIS_URL: str | None = os.getenv("REDIS_URL")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Enforce strong secrets in staging/production
    @field_validator("secret_key")
    @classmethod
    def _validate_secret_key(cls, v: str) -> str:
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be >=32 chars.")
        return v

    @field_validator("API_KEY")
    @classmethod
    def _validate_api_key(cls, v: str) -> str:
        env = os.getenv("APP_ENV", "development").strip().lower()
        if env in {"staging", "production"}:
            if v.lower() in {"change-me", "dev-key"} or len(v) < 24:
                raise ValueError("API_KEY too weak for staging/production.")
        return v

    model_config = SettingsConfigDict(
        env_file=None,  # we already loaded the right file via load_dotenv
        env_file_encoding="utf-8",
        extra="forbid",
    )


settings = Settings()
