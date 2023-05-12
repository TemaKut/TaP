from datetime import datetime

from pydantic import BaseModel


class PhotoCreate(BaseModel):
    """ Схема данных при создании фотографии. """

    description: str = None


class PhotoGetSchema(BaseModel):
    """ Схема фотографии для response. """

    id: int
    image_uri: str
    description: str = None
    owner_id: int
    added_at: datetime

    class Config:
        orm_mode = True
