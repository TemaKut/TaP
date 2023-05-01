import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.settings import settings
from app.main import app
from app.api.users.models import User
from app.database.base import get_async_session


async_engine = create_async_engine(settings.TEST_DB_URL, future=True)

Session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop(request):
    """ Дополнительный event loop для тестов """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def setup_db(request):
    """ Создать БД с необходимыми таблицами, а послу всех тестов удалить. """
    async with async_engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)


@pytest.fixture(scope='function')
async def client():
    """ Фикстура создаёт объект клиента приложения fastapi. """

    async def get_async_session_new() -> AsyncSession:
        """ Получить объект асинхронной сессии БД, а следом закрыть её. """
        session = Session()

        try:
            yield session

        except Exception:
            await session.rollback()

        finally:
            await session.close()

    app.dependency_overrides[get_async_session] = get_async_session_new

    async with AsyncClient(app=app, base_url="http://test") as client_:
        yield client_


@pytest.fixture(scope='function')
async def session() -> AsyncSession:
    """ Получить объект асинхронной сессии БД, а следом закрыть её. """
    session = Session()

    try:
        yield session

    except Exception as e:
        print(f'Error with async session: {e}')
        await session.rollback()

    finally:
        await session.close()
