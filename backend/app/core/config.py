from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Aarogya360"
    debug: bool = False

    database_url: str = Field(
        default="postgresql://postgres:admin123@localhost/Aarogya360",
        alias="DATABASE_URL",
    )

    secret_key: str = Field(
        default="CHANGE-ME-IN-PRODUCTION-USE-STRONG-RANDOM-SECRET",
        alias="SECRET_KEY",
    )
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

    bcrypt_rounds: int = Field(default=12, alias="BCRYPT_ROUNDS")

    @field_validator("refresh_token_expire_days")
    @classmethod
    def validate_refresh_days(cls, value: int) -> int:
        if not 7 <= value <= 30:
            raise ValueError("REFRESH_TOKEN_EXPIRE_DAYS must be between 7 and 30")
        return value

    @property
    def async_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if url.startswith("postgresql+psycopg2://"):
            return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
        if url.startswith("sqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
