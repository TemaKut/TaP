from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt

from app.database.base import get_async_session
from .models import User
from app.settings import log, settings
from .schemas import (
    UserCreateSchema,
    UserGetSchema,
    TokenCreateSchema,
    TokenGetSchema,
)
from . import bad_responses as br


class UsersCRUD():
    """ CRUD operations with users. """

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        """ Инициализация объекта класса. """
        self.session = session

    async def get_list_of_users(self):
        """ Получить список всех пользователей из БД. """
        query = select(User)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_user_from_db(self, username: str) -> User:
        """ Получить пользователя из БД. """
        query = select(User).where(User.username == username)

        try:
            result = await self.session.execute(query)
            result = result.scalars().all()

        except Exception:
            log.error('Incorrect username')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=br.UserNotFound().dict(),
            )

        if len(result) == 1:

            return result[0]

        log.error('User not in DB')
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=br.UserNotFound().dict(),
            )

    async def create_user(self, data: UserCreateSchema) -> UserGetSchema:
        """ Создать пользоваетеля. """
        if await self._is_user_in_db(data.username):
            log.error('User alredy exists.')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=br.UserAlredyExists().dict(),
            )

        user = User(**data.dict())

        try:
            self.session.add(user)
            await self.session.commit()

        except Exception:
            log.critical('Error with add user in DB')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=br.UserAddInDbError().dict(),
            )

        return UserGetSchema.from_orm(user)

    async def create_token(self, data: TokenCreateSchema) -> TokenGetSchema:
        """ Создание токена пользователя. """
        # Получение и верификация пользователя
        user: User = await self.get_user_from_db(data.username)
        user.verify_password(data.password)

        # Формирование данных токена
        user_data = UserGetSchema.from_orm(user).dict()
        now = datetime.utcnow()

        token_data = {
            "iat": now,
            "exp": now + timedelta(seconds=settings.JWT_EXPIRE_SEC),
            'user_id': user.id,
            'user': user_data,
        }

        # Кодирование данных в токен
        token = jwt.encode(
            token_data,
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        return TokenGetSchema(token=token)

    async def _is_user_in_db(self, username: str):
        """ Проверка существует ли пользователь в БД """
        query = select(User).where(User.username == username)

        result = await self.session.execute(query)
        result = result.fetchall()

        return True if len(result) > 0 else False
