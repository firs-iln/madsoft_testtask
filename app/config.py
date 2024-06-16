from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class DBSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def db_uri(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(env_file='../app/db.env', env_file_encoding='utf-8')


class MediaSettings(BaseSettings):
    MEDIASERVER_HOST: str
    MEDIASERVER_PORT: str

    @property
    def mediaserver_uri(self):
        return f"http://{self.MEDIASERVER_HOST}:{self.MEDIASERVER_PORT}/media"

    model_config = SettingsConfigDict(env_file='../app/media.env', env_file_encoding='utf-8')


class AppSettings(BaseSettings):
    IS_SECURE: bool
    HOST: str

    model_config = SettingsConfigDict(env_file='../app/.env', env_file_encoding='utf-8')


db_config = DBSettings()
media_config = MediaSettings()
app_config = AppSettings()
