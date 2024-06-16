from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

Schema = TypeVar("Schema", bound=BaseModel, covariant=True)
SQLModel = TypeVar("SQLModel", bound=DeclarativeBase, covariant=True)
