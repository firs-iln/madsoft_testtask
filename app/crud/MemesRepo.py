from crud.AbstractRepo import AbstractRepo
from crud.schemas import MemeCreate, MemeResponse, MemeUpdate
from database.models import Meme


class MemesRepo(AbstractRepo):
    model = Meme
    update_schema = MemeUpdate
    create_schema = MemeCreate
    get_schema = MemeResponse
