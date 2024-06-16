from contextlib import asynccontextmanager

from crud.MemesRepo import MemesRepo
from database import get_session


@asynccontextmanager
async def get_memes_repo() -> MemesRepo:
    async with get_session() as session:
        yield MemesRepo(session=session)
