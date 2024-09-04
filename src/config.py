from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, extra="allow")

    LOGIN: str
    PASSWORD: str
    TRINKET_BASE_URL: str = "https://trinket.io"

    DEBUG: str

    @property
    def debug(self) -> bool:
        return self.DEBUG == "True"


settings = Settings()
