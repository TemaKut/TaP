import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from httpx import AsyncClient

from app.api.users.models import User
from app.main import app


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
    result = result.scalars().unique().all()

    return len(result) == 1


async def get_auth_header_for_user(
    client: AsyncClient,
    username: str,
    password: str,
) -> str:
    """ Получить токен пользователя через соответствующий эндпоинт. """
    data = {
        'username': username,
        'password': password,
    }
    uri = app.url_path_for('get-token')
    response = await client.post(uri, json=data)
    response = json.loads(response.text)

    token = response.get('token')
    token_type = response.get('token_type')
    assert token

    data = {'Authorization': f'{token_type} {token}'}

    return data
