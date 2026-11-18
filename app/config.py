from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    gemini_api_key: str = ""
    app_host: str = "0.0.0.0"
    app_port: int = 4000
    max_content_length: int = 50000
    request_timeout: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
