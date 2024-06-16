from contextlib import contextmanager
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from crud.exceptions import NotFoundException
from crud.schemas import MemeResponse
from dependencies.services import get_memes_service
from services import MemesService
from starlette.testclient import TestClient

from app import app


@pytest.fixture
def mock_memes_repo():
    mock_repo = MagicMock(spec=MemesService)

    memes = [
        MemeResponse(id=uuid4(), title=f"Test Meme {i}", description="Testing mock memes", image="mock_image_url",
                     created_at=datetime.now(), updated_at=datetime.now())
        for i in range(10)
    ]

    async def create(schema, **kwargs):
        meme = MemeResponse(id=uuid4(), title=schema.title, description=schema.description, image="mock_image_url",
                            created_at=datetime.now(), updated_at=datetime.now())
        memes.append(meme)
        return meme

    async def get(record_id):
        meme = list(filter(lambda x: x.id == record_id, memes))
        if not meme:
            raise NotFoundException(f"There is no entity Meme with id {record_id}")
        return meme[0]

    async def update(record_id, schema, **kwargs):
        for meme in memes:
            if meme.id == record_id:
                meme.title = schema.title
                meme.description = schema.description
                meme.updated_at = datetime.now()
                return meme
        return None

    async def delete(record_id):
        for meme in memes:
            if meme.id == record_id:
                memes.remove(meme)

    async def get_all(page, size):
        start = page * size if page * size < len(memes) else len(memes)
        end = (page + 1) * size if (page + 1) * size < len(memes) else len(memes)
        return memes[start:end]

    mock_repo.create = create
    mock_repo.get = get
    mock_repo.update = update
    mock_repo.delete = delete
    mock_repo.get_all = get_all

    return mock_repo


@contextmanager
def patch_app(mock):
    def amock_get_memes_repo():
        nonlocal mock

        return mock

    try:
        app.dependency_overrides[get_memes_service] = amock_get_memes_repo
        yield
    finally:
        app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_meme(mock_memes_repo):
    create_schema = {
        "title": "Test Meme",
        "description": "Testing meme creation",
    }

    test_image_name = "test_image.png"
    with open(test_image_name, "rb") as image:
        content = {
            "image": (test_image_name, image, "image/png"),
        }
        with patch_app(mock_memes_repo):
            response = TestClient(app).post(
                "/memes/",
                data=create_schema,
                files=content,
            )

    assert response.status_code == 200

    meme_id = response.json()["id"]
    with patch_app(mock_memes_repo):
        response = TestClient(app).get(f"/memes/{meme_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(meme_id)
    assert response.json()["title"] == create_schema["title"]


@pytest.mark.asyncio
async def test_create_meme(mock_memes_repo):
    create_schema = {
        "title": "Test Meme",
        "description": "Testing meme creation",
    }

    test_image_name = "test_image.png"
    with open(test_image_name, "rb") as image:
        content = {
            "image": (test_image_name, image, "image/png"),
        }
        with patch_app(mock_memes_repo):
            response = TestClient(app).post(
                "/memes/",
                data=create_schema,
                files=content,
            )

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == create_schema["title"]


@pytest.mark.asyncio
async def test_update_meme(mock_memes_repo):
    create_schema = {
        "title": "Test Meme",
        "description": "Testing meme creation",
    }

    test_image_name = "test_image.png"
    with open(test_image_name, "rb") as image:
        content = {
            "image": (test_image_name, image, "image/png"),
        }

        with patch_app(mock_memes_repo):
            response = TestClient(app).post(
                "/memes/",
                data=create_schema,
                files=content,
            )

    assert response.status_code == 200

    meme_id = response.json()["id"]

    update_schema = {
        "title": "Updated Meme",
        "description": "Testing meme update",
        'image': '',
    }

    with open(test_image_name, "rb") as image:
        content = {
            "image": (test_image_name, image, "image/png"),
        }

        with patch_app(mock_memes_repo):
            response = TestClient(app).put(f"/memes/{meme_id}", data=update_schema, files=content,
                                           )

    assert response.status_code == 200
    assert response.json()["title"] == update_schema["title"]


def test_delete_meme(mock_memes_repo):
    create_schema = {
        "title": "Test Meme",
        "description": "Testing meme creation",
    }

    test_image_name = "test_image.png"
    with open(test_image_name, "rb") as image:
        content = {
            "image": (test_image_name, image, "image/png"),
        }

        with patch_app(mock_memes_repo):
            response = TestClient(app).post(
                "/memes/",
                data=create_schema,
                files=content,
            )

    assert response.status_code == 200

    meme_id = response.json()["id"]

    with patch_app(mock_memes_repo):
        response = TestClient(app).delete(f"/memes/{meme_id}")

    assert response.status_code == 200

    with patch_app(mock_memes_repo):
        response = TestClient(app).get(f"/memes/{meme_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_memes(mock_memes_repo):
    with patch_app(mock_memes_repo):
        response = TestClient(app).get("/memes/", params={"page": 0, "size": 10})

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "id" in response.json()[0]
