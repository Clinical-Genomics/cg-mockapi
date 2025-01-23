from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    lims_host: str

    model_config = SettingsConfigDict(
        env_mapping={
            "lims_host": "LIMS_HOST",
        },
    )


settings = Settings()
settings = Settings()
