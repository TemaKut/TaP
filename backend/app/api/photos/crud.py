from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_async_session
from app.api.users.models import User
from .models import Photo
from .schemas import PhotoCreate


class PhotosCRUD():
    """ Методы для работы с таблицей БД Photos """

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        """ Инициализация объекта класса. """
        self.session = session

    async def deploy_photo(self, photo_data: PhotoCreate, user: User) -> Photo:
        """ Добавить фотографию с описанием в БД """

        photo = Photo(owner_id=user.id, **photo_data.dict())

        self.session.add(photo)
        await self.session.commit()
