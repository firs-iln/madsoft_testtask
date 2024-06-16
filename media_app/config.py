from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioConfig(BaseSettings):
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: SecretStr
    BUCKET_NAME: str
    ACCESS_KEY: SecretStr
    SECRET_KEY: SecretStr
    ENDPOINT_URL: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


minio_config = MinioConfig()
