import logging
import os

from _utils import clean
from dependencies import get_storage_client
from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                     UploadFile)
from fastapi.responses import FileResponse
from storage import StorageClient
from storage.exceptions import (DeletingError, DownloadingError, NoSuchKey,
                                UploadingError)

router = APIRouter(
    prefix="/media",
    tags=["media/"],
)

logger = logging.getLogger(__name__)


@router.post('')
async def add_media(
        file: UploadFile = File(...),
        storage: StorageClient = Depends(get_storage_client),
) -> dict[str, str]:
    async with clean(file):
        try:
            path = await storage.upload_file(file.filename)
        except UploadingError:
            raise HTTPException(500, "Unknown error from storage")

    return {'filename': path}


@router.delete('')
async def delete_media(
        filename: str,
        storage: StorageClient = Depends(get_storage_client),
):
    try:
        await storage.delete_file(filename)
    except NoSuchKey:
        raise HTTPException(404, "No such key")
    except DeletingError:
        raise HTTPException(500, "Unknown error from storage")


@router.get('')
async def get_media(
        filename: str,
        background_tasks: BackgroundTasks,
        storage: StorageClient = Depends(get_storage_client),
) -> FileResponse:
    try:
        file_path = await storage.get_file(filename)
        background_tasks.add_task(os.remove, file_path)
        response = FileResponse(path=file_path, filename=file_path, media_type='multipart/form-data')
    except NoSuchKey:
        raise HTTPException(404, "No such key")
    except DownloadingError:
        raise HTTPException(500, "Unknown error from storage")

    return response
