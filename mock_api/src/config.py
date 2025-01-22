from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    lims_host: str

    model_config = SettingsConfigDict(
        env_file=str(dotenv_path),
        env_file_encoding="utf-8",
        env_mapping={
            "lims_host": "LIMS_HOST",
        },
    )


settings = Settings()
