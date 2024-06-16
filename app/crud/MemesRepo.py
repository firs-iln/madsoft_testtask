from crud.AbstractRepo import AbstractRepo
from database.models import Meme
from crud.schemas import MemeResponse, MemeCreate, MemeUpdate


class MemesRepo(AbstractRepo):
    model = Meme
    update_schema = MemeUpdate
    create_schema = MemeCreate
    get_schema = MemeResponse
