from pydantic import Field
from pydantic_settings import BaseSettings

__all__ = [
    "settings",
]


class Settings(BaseSettings):
    TARGET_HOST: str = Field(default="http://localhost:8000")


settings = Settings()
