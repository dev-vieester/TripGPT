from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "TripGPT"
    app_version: str = "0.1.0"
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL")
    openrouter_api_key: str | None = Field(default=None, alias="OPENROUTER_API_KEY")
    gemini_model: str | None = Field(default=None, alias="GEMINI_MODEL")
    google_model: str | None = Field(default=None, alias="GOOGLE_MODEL")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()