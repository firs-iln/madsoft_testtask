from typing import Type
from uuid import UUID

from crud import Schema
from crud.AbstractRepo import AbstractRepo


class AbstractService:
    repo_type: Type[AbstractRepo] = AbstractRepo

    def __init__(self, repo: repo_type):
        self.repository = repo

    async def get(self, record_id: UUID, *args, **kwargs) -> repo_type.get_schema:
        return await self.repository.get(record_id=record_id)

    async def get_all(self, page: int = 0, size: int = 100, *args, **kwargs) -> list[repo_type.get_schema]:
        return await self.repository.get_all(page=page, size=size)

    async def create(self, schema: Schema, *args, **kwargs) -> repo_type.get_schema:
        return await self.repository.create(schema=schema)

    async def update(self, record_id: UUID, schema: Schema, *args, **kwargs) -> repo_type.get_schema:
        return await self.repository.update(record_id=record_id, schema=schema)

    async def delete(self, record_id: UUID, *args, **kwargs) -> None:
        await self.repository.delete(record_id=record_id)
