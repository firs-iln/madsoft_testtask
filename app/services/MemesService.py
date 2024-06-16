from uuid import UUID

from config import app_config
from crud import Schema
from crud.MemesRepo import MemesRepo
from crud.schemas import MemeUpdate
from fastapi import UploadFile
from media import MediaRepo
from services.AbstractService import AbstractService


class MemesService(AbstractService):
    repo_type = MemesRepo

    async def create(self, schema: Schema, image: UploadFile, *args, **kwargs) -> repo_type.get_schema:
        meme = await super().create(schema)

        await MediaRepo.upload(filename=str(meme.id), file=image)

        update_schema = MemeUpdate(**meme.model_dump())

        link = f"{'https' if app_config.IS_SECURE else 'http'}://{app_config.HOST}/memes/file/{meme.id}"
        update_schema.image = link
        return await super().update(record_id=meme.id, schema=update_schema)

    async def update(self, record_id: UUID, image: UploadFile, schema: Schema, *args, **kwargs) -> repo_type.get_schema:
        current_meme = await super().get(record_id=record_id)

        meme_link = await MediaRepo.upload(filename=current_meme.title, file=image)

        update_schema = MemeUpdate(**schema.to_dict())
        update_schema.image = meme_link

        return await super().update(record_id=record_id, schema=update_schema)

    async def delete(self, record_id: UUID, *args, **kwargs) -> None:
        await super().get(record_id=record_id)

        await MediaRepo.delete(filename=str(record_id))
        await super().delete(record_id=record_id)

    async def get_image(self, meme_id: UUID) -> str:
        await super().get(record_id=meme_id)

        return await MediaRepo.get_file(str(meme_id))
