from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_async_session
from app.api.users.models import User


class PhotosCRUD():
    """ Методы для работы с таблицей БД Photos """

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        """ Инициализация объекта класса. """
        self.session = session

    async def upload_photo(file: UploadFile, user: User):
        """ Добавить фотографию с описанием в БД """

        return 1
