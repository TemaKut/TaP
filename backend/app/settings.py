import os

from pydantic import BaseSettings
from loguru import logger
from dotenv import load_dotenv

# Подгрузить данные из .env
load_dotenv()


class Settings(BaseSettings):
    """ Класс настроек для приложения. """
    DB_URL: str = os.getenv('DB_URL')

    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    JWT_EXPIRE_SEC: int = os.getenv('JWT_EXPIRE_SEC')
    JWT_SECRET: str = os.getenv('JWT_SECRET')

    TEST_DB_URL = os.getenv('TEST_DB_URL')

    @property
    def log(self):
        """ Логгер приложения. """
        logger.remove()
        logger.add(
            "logs/logs.log",
            level='DEBUG',
            rotation="2 MB",
            format=(
                "{time:YYYY-MM-DD at HH:mm:ss} "
                "| {level} | {name} {line} | {message}"
            ),
        )

        return logger


# Объект настроек. Обращение только через него.
settings = Settings()

# Объект логгера. Все логи через него
log = settings.log
