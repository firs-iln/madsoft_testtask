from contextlib import asynccontextmanager
from typing import AsyncGenerator

from config import db_config
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

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
