from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.settings import settings, log


async_engine = create_async_engine(settings.DB_URL, future=True)

Session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()


async def get_async_session() -> AsyncSession:
    """ Получить объект асинхронной сессии БД, а следом закрыть её. """
    session = Session()

    try:
        yield session

    except Exception as e:
        log.critical(f'Error with async session: {e}')
        await session.rollback()

    finally:
        await session.close()
