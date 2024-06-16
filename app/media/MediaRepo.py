import os
from contextlib import asynccontextmanager

from fastapi import UploadFile
from httpx import AsyncClient as client
from config import media_config
from media.exceptions import MediaserverError, NoSuchKey


class MediaRepo:
    @staticmethod
    async def upload(filename: str, file: UploadFile) -> None:
        async with client() as c:
            response = await c.post(
                media_config.mediaserver_uri,
                files={"file": (filename, file.file, file.content_type)},
            )

        if not response.status_code == 200:
            raise MediaserverError(f"An error occurred while uploading file.\nStatus code: {response.status_code}\nDetails: {response.reason_phrase}")

    @staticmethod
    async def delete(filename: str) -> None:
        async with client() as c:
            response = await c.delete(
                media_config.mediaserver_uri,
                params={"filename": filename},
            )
        if response.status_code == 404:
            raise NoSuchKey(f"There is no object with key {filename}")

        elif not response.status_code == 200:
            raise MediaserverError(f"An error occurred while deleting file.\nStatus code: {response.status_code}\nDetails: {response.reason_phrase}")

    @staticmethod
    async def get_file(filename: str):
        async with client() as c:
            response = await c.get(
                media_config.mediaserver_uri,
                params={"filename": filename},
            )

        if response.status_code == 404:
            raise NoSuchKey(f"There is no object with key {filename}")

        elif not response.status_code == 200:
            raise MediaserverError(f"An error occurred while getting file.\nStatus code: {response.status_code}\nDetails: {response.reason_phrase}")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename
