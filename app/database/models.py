import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Meme(Base):
    __tablename__ = 'memes'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda x: uuid.uuid4().hex)
    title: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]
