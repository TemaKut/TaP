from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from . import bad_responses as br
from .models import User
from app.settings import log, settings
from app.database.base import get_async_session


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """ Получить объект пользователя из БД, выполневшего запрос. """
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=br.AuthenticationRequired().dict(),
    )
    # Получение токена авторизации из запроса
    try:
        token = request._headers.get('authorization').split(' ')[1]

    except Exception as e:
        log.error(f'Authorization required. {e}')
        raise error

    # Расшифровка токена
    try:
        token_data = jwt.decode(
            token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

    except JWTError as e:
        log.error(f'Invalid token {e}')
        raise error

    try:
        user_id = token_data['user_id']
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise

    except Exception as e:
        log.error(f'Cant get from DB {e}')
        raise error

    return user
