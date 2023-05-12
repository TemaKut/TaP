import os
import aiofiles as af
from datetime import datetime as dt

from fastapi import Depends, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_async_session
from app.api.users.models import User
from app.settings import settings, log


class PhotosCRUD():
    """ Методы для работы с таблицей БД Photos """

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        """ Инициализация объекта класса. """
        self.session = session

    async def upload_photo(self, file: UploadFile, user: User):
        """ Добавить фотографию с описанием в БД """
        if not os.path.exists(settings.MEDIA_DIR):
            log.critical('Media dir not created')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Media dir not created'
            )
        file = await self._check_file_type(file)

        uri, path = await self._create_media_uri(file, user)

        # В медиа директории пользователя создать файл изображения
        # И записать в него байты переданного файла
        async with af.open(path, 'w+b') as image:
            await image.write(file.file.read())

        return uri

    async def _check_file_type(self, file: UploadFile) -> UploadFile:
        """ Возбудить исключение в случае если тип файла не соответствует. """
        allowed_file_types = [
            'image/jpeg',
            'image/png',
        ]

        if not file.headers.get('content-type') in allowed_file_types:
            log.error('Photo was not created. Error photo type')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Allowed types is {allowed_file_types}'
            )

        return file

    async def _create_media_uri(self, file: UploadFile, user: User) -> str:
        """
        Создать ссылку для дальнейшего сохранения файла,
        а так же для дальнейшего к ней обрращения через http.
        """
        now_sec_str = str(dt.now().timestamp()).replace('.', '')
        file_extantion = file.headers.get('content-type').split('/')[-1]
        filename = f'{now_sec_str}.{file_extantion}'

        username = user.username

        # Создать директорию пользователя в случае отсутствия
        user_dir = f'{settings.MEDIA_DIR}/{username}'

        if not os.path.exists(user_dir):
            os.mkdir(user_dir)

        path = os.path.join(settings.MEDIA_DIR, username, filename)

        return (f'{username}/{filename}', path)
