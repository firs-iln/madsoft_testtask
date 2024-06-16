from typing import Type
from uuid import UUID

from crud import Schema, SQLModel
from crud.exceptions import InvalidSchemaError, NotFoundException
from sqlalchemy import delete, inspect, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepo:
    model: Type[SQLModel] = SQLModel
    update_schema: Type[Schema] = Schema
    create_schema: Type[Schema] = Schema
    get_schema: Type[Schema] = Schema

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, record_id: UUID) -> get_schema:
        try:
            res = await self.session.execute(select(self.model).where(inspect(self.model).primary_key[0] == record_id))
            obj = res.scalar_one()
            if not obj:
                raise NotFoundException(f"There is no entity {self.model.__name__} with id {record_id}")

            return self.get_schema.model_validate(obj)

        except NoResultFound:
            raise NotFoundException(f"There is no entity {self.model.__name__} with id {record_id}")

    async def get_all(self, page: int = 0, size: int = 100) -> list[get_schema]:
        offset = page * size
        limit = size
        res = await self.session.execute(select(self.model).offset(offset).limit(limit))
        objects = res.scalars().all()
        return [self.get_schema.model_validate(obj) for obj in objects]

    async def create(self, schema: Schema) -> get_schema:
        if not schema:
            raise InvalidSchemaError("Schema is required")

        instance = self.model(**schema.model_dump())
        self.session.add(instance)
        await self.session.commit()

        await self.session.refresh(instance)
        return self.get_schema.model_validate(instance)

    async def update(self, record_id: UUID, schema: Schema) -> get_schema:
        if not schema:
            raise InvalidSchemaError("Schema is required")

        clean_kwargs = {key: value for key, value in schema.model_dump().items() if value is not None}
        if not clean_kwargs:
            raise InvalidSchemaError("No valid data to update")

        await self.session.execute(
            update(self.model).where(inspect(self.model).primary_key[0] == record_id).values(**clean_kwargs))
        await self.session.commit()

        return await self.get(record_id)

    async def delete(self, record_id: UUID) -> None:
        await self.session.execute(delete(self.model).where(inspect(self.model).primary_key[0] == record_id))
        await self.session.commit()
