import os
from uuid import UUID

from crud.exceptions import InvalidSchemaError, NotFoundException
from crud.schemas import MemeCreate, MemeResponse, MemeUpdate
from dependencies import get_memes_service
from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                     Query, UploadFile)
from fastapi.responses import FileResponse
from media.exceptions import MediaserverError, NoSuchKey
from routes.schemas import CreateMeme, UpdateMeme
from services.MemesService import MemesService

router = APIRouter(
    prefix='/memes',
    tags=['memes'],
)


@router.get('/{meme_id}')
async def get_one(
        meme_id: UUID,
        memes: MemesService = Depends(get_memes_service),
) -> MemeResponse:
    try:
        return await memes.get(record_id=meme_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f'There is no meme with id {meme_id}')


@router.get('')
async def get_all(
        page: int = Query(0, ge=0),
        size: int = Query(10, ge=1, le=100),
        memes: MemesService = Depends(get_memes_service),
) -> list[MemeResponse]:
    return await memes.get_all(page=page, size=size)


@router.post('')
async def create(
        meme: CreateMeme = Depends(),
        image: UploadFile = File(...),
        memes: MemesService = Depends(get_memes_service),
) -> MemeResponse:
    try:
        create_schema = MemeCreate(**meme.to_dict(), image='')
        res = await memes.create(schema=create_schema, image=image)
    except InvalidSchemaError:
        raise HTTPException(status_code=400, detail='Invalid schema')

    return res


@router.put('/{meme_id}')
async def update(
        meme_id: UUID,
        meme: UpdateMeme = Depends(),
        image: UploadFile = File(...),
        memes: MemesService = Depends(get_memes_service),
) -> MemeResponse:
    try:
        update_model = MemeUpdate(**meme.to_dict(), image='')
        res = await memes.update(record_id=meme_id, image=image, schema=update_model)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f'There is no meme with id {meme_id}')
    except InvalidSchemaError:
        raise HTTPException(status_code=400, detail='Invalid schema')

    return res


@router.delete('/{meme_id}')
async def delete(
        meme_id: UUID,
        memes: MemesService = Depends(get_memes_service),
):
    try:
        await memes.delete(meme_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f'There is no meme with id {meme_id}')
    except NoSuchKey:
        ...


@router.get("/file/{meme_id}")
async def get_file(
        meme_id: UUID,
        background_tasks: BackgroundTasks,
        memes: MemesService = Depends(get_memes_service)
) -> FileResponse:
    try:
        file_path = await memes.get_image(meme_id=meme_id)

        background_tasks.add_task(os.remove, file_path)

        return FileResponse(path=file_path, filename=str(meme_id), media_type='multipart/form-data')

    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"There is no meme with id {meme_id}")
    except NoSuchKey:
        raise HTTPException(status_code=500,
                            detail=f"Something went wrong. There is no picture for meme with id {meme_id}")
    except MediaserverError:
        raise HTTPException(status_code=500, detail="Mediaserver is currently unavailable, try again later")
