from dependencies.repositories import get_memes_repo
from services import MemesService


async def get_memes_service() -> MemesService:
    async with get_memes_repo() as repo:
        yield MemesService(repo=repo)

