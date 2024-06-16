from dataclasses import dataclass
from typing import Optional

from fastapi import Form


@dataclass
class CreateMeme:
    title: str = Form(...)
    description: str = Form(...)

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description
        }


@dataclass
class UpdateMeme:
    title: Optional[str] = Form(...)
    description: Optional[str] = Form(...)

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description
        }
