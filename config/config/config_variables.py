from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the config directory
CONFIG_DIR = Path(__file__).parent


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'env' / 'data_credentials.env'),
        env_file_encoding='utf-8',
    )

    api_key: str


data_credentials_config = Config()
