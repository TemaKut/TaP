from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.users.models import User


async def create_user(
    session: AsyncSession,
    username: str,
    password: str = 'password',
):
    """ Создать пользователя в БД """
    user = User(username=username, password=password)
    session.add(user)
    await session.commit()


async def check_user_in_db(username: str, session: AsyncSession):
    """ Проверить появился ли пользователь в БД """
    query = select(User).filter_by(username=username)
    result = await session.execute(query)
    result = result.scalars().all()

    return len(result) == 1
