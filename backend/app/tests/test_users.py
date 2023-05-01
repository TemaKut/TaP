import json

from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from fastapi import status

from app.main import app
from .utils import create_user, check_user_in_db


async def test_user_create_in_db(
    session: AsyncSession,
    client: AsyncClient,
):
    """ Попал ли пользователь в БД при его создании через эндпоинт. """
    username = "Artem"
    data = {"username": username, "password": "string"}

    uri = app.url_path_for('create_user')
    response = await client.post(uri, json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert await check_user_in_db(username, session)


async def test_user_create_alredy_exists(
    session: AsyncSession,
    client: AsyncClient,
):
    """ При создании двух одинаковых пользователей выбрасывается ошибка. """
    username = "Artem"
    data = {"username": username, "password": "string"}

    uri = app.url_path_for('create_user')
    response = await client.post(uri, json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert await check_user_in_db(username, session)

    response2 = await client.post(uri, json=data)

    assert response2.status_code == status.HTTP_400_BAD_REQUEST


async def test_get_token(
    session: AsyncSession,
    client: AsyncClient,
):
    """ Выдаётся ли токен зарегестрированному пользователю через эндпоинт """
    # Создать пользователя в БД
    username = "Artem"
    password = 'password'
    await create_user(session, username, password=password)

    # Проверить создался ли пользователь
    assert await check_user_in_db(username, session)

    # Запрос на соответствующий эндпоинт
    data = {
        'username': username,
        'password': password,
    }
    uri = app.url_path_for('get-token')
    response = await client.post(uri, json=data)

    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.text)

    assert response_data.get('token')
    assert response_data.get('token_type')


async def test_get_list_of_users(
    session: AsyncSession,
    client: AsyncClient,
):
    """ Проверка эндпоинта получения списка всех пользователей """
    usernames = ['Trgq1', 'eft2', 'Artet3']

    for username in usernames:
        # Создать пользователя
        await create_user(session, username)

        # Проверить создался ли пользователь
        assert await check_user_in_db(username, session)

    uri = app.url_path_for('get_list_of_users')

    response = await client.get(uri)

    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.text)

    assert len(response_data) == len(usernames)


async def test_get_user_by_username(
    session: AsyncSession,
    client: AsyncClient,
):
    """ Тест эндпоинта получения пользователя по username. """
    username = 'Artem'

    uri = app.url_path_for('get_user_by_username', username=username)
    response = await client.get(uri)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Создадим пользователя с тем же username
    await create_user(session, username)
    assert await check_user_in_db(username, session)

    uri = app.url_path_for('get_user_by_username', username=username)
    response = await client.get(uri)

    assert response.status_code == status.HTTP_200_OK
