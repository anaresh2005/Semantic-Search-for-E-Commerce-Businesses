from pathlib import Path
from pydantic import SecretStr 
from pydantic import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parent.parent / ".env"
class Settings(BaseSettings):
    # Environment variables
    model_config = SettingsConfigDict(
        env_file = str(ENV_FILE),
        env_file_encoding = "utf-8",
    )

    # OpenAI API key
    OPENAI_MODEL_ID: str = "gpt-4o"
    OPENAI_API_KEY: SecretStr

    # Gemini API key
    GEMINI_API_KEY: SecretStr | None = None
    GEMINI_MODEL_ID: str = "gemini-embedding-001"

settings = Settings()