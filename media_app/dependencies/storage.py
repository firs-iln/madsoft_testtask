from config import minio_config
from storage import S3Client


def get_storage_client() -> S3Client:
    return S3Client(
        access_key=minio_config.ACCESS_KEY.get_secret_value(),
        secret_key=minio_config.SECRET_KEY.get_secret_value(),
        endpoint_url=minio_config.ENDPOINT_URL,
        bucket_name=minio_config.BUCKET_NAME,
    )

