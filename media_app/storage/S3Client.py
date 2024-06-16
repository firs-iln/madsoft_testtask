import logging
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from storage.StorageClient import StorageClient
from storage.exceptions import UploadingError, DeletingError, DownloadingError, NoSuchKey

logger = logging.getLogger(__name__)


class S3Client(StorageClient):
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
    ) -> str:
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )

                logger.info(f"File {object_name} uploaded to {self.bucket_name}")

            return await self._get_file_url(object_name)

        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise UploadingError(f"Error uploading file {object_name}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File {object_name} deleted from {self.bucket_name}")

        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                raise NoSuchKey(f"There is no object with key {object_name}")

            logger.error(f"Error deleting file: {e}")
            raise DeletingError(f"Error deleting file {object_name}")

    async def get_file(self, object_name: str) -> str:
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(object_name, "wb") as file:
                    file.write(data)

                logger.info(f"File {object_name} downloaded to {object_name}")
                return object_name

        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                raise NoSuchKey(f"There is no object with key {object_name}")

            logger.error(f"Error downloading file: {e}")
            raise DownloadingError(f"Error downloading file {object_name}")

    async def _get_file_url(self, object_name: str) -> str:
        return f"{self.config['endpoint_url']}/{self.bucket_name}/{object_name}"
