from contextlib import contextmanager
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.crud.exceptions import NotFoundException
from app.crud.schemas import MemeResponse
from app.dependencies import get_memes_service
from app.main import app
from app.services import MemesService


@pytest.fixture
def mock_memes_service():
    mock_service = MagicMock(spec=MemesService)

    memes = [
        MemeResponse(id=uuid4(), title=f"Test Meme {i}", description="Testing mock memes", image="mock_image_url",
                     created_at=datetime.now(), updated_at=datetime.now())
        for i in range(10)
    ]

    async def create(schema):
        meme = MemeResponse(id=uuid4(), title=schema.title, description=schema.description, image="mock_image_url",
                            created_at=datetime.now(), updated_at=datetime.now())
        memes.append(meme)
        return meme

    async def get(record_id):
        meme = list(filter(lambda x: x.id == record_id, memes))
        if not meme:
            raise NotFoundException(f"There is no entity Meme with id {record_id}")
        return meme[0]

    async def update(record_id, schema):
        for meme in memes:
            if meme.id == record_id:
                meme.title = schema.title
                meme.description = schema.description
                meme.updated_at = datetime.now()
                return meme
        return None

    async def delete(record_id):
        for meme in memes:
            if meme.id == record_id:
                memes.remove(meme)

    async def get_all(page, size):
        start = page * size if page * size < len(memes) else len(memes)
        end = (page + 1) * size if (page + 1) * size < len(memes) else len(memes)
        return memes[start:end]

    mock_service.create = create
    mock_service.get = get
    mock_service.update = update
    mock_service.delete = delete
    mock_service.get_all = get_all

    return mock_service

