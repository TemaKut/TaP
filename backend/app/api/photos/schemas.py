from pydantic import BaseModel


class PhotoCreate(BaseModel):
    """ Схема данных при создании фотографии. """

    data: bytes
    description: str = None
