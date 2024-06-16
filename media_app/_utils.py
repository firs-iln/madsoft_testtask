import os
from contextlib import asynccontextmanager

from fastapi import UploadFile


@asynccontextmanager
async def clean(file: UploadFile):
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    yield

    os.remove(file.filename)
