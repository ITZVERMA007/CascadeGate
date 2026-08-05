# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict


# Checks for env values
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    GROQ_API_KEY: str
    OPENAI_API_KEY: str

    API_KEY: str

    CONFIDENCE_THRESHOLD: float = -1.0
    RATE_LIMIT_PER_MINUTE: int = 30
    LOG_LEVEL: str = "INFO"

    # Reading the values from the env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
