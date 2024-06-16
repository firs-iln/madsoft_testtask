from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MemeUpdate(BaseModel):
    title: str
    description: str
    image: str

    model_config = ConfigDict(from_attributes=True)


class MemeCreate(MemeUpdate):
    pass


class MemeResponse(MemeCreate):
    id: UUID
    image: str
    created_at: datetime
    updated_at: datetime
