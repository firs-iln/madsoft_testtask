from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import db_config

from typing import AsyncGenerator

engine = create_async_engine(
    db_config.db_uri,
)

sessionmaker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = sessionmaker()
    try:
        yield session
    finally:
        await session.close()
