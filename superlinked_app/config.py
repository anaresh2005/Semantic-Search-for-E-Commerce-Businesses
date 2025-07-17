from pathlib import Path
from loguru import logger
from pydantic import SecretStr
from pydantic import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / ".env"
logger.info(f"Loading .env file from: {ENV_FILE}")


class Settings(BaseSettings):
    # Environment variables
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
    )

    # OpenAI API key
    OPENAI_MODEL_ID: str = "gpt-4o"
    OPENAI_API_KEY: SecretStr

    # Gemini API key
    GEMINI_MODEL_ID: str = "gemini-embedding-001"
    GEMINI_API_KEY: SecretStr


settings = Settings()
