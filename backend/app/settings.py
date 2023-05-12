import os
from pathlib import Path

from pydantic import BaseSettings
from loguru import logger
from dotenv import load_dotenv

# Подгрузить данные из .env
load_dotenv()

BASE_DIR = os.path.realpath((Path(__file__).resolve().parent))


class Settings(BaseSettings):
    """ Класс настроек для приложения. """
    DB_URL: str = os.getenv('DB_URL')
    TEST_DB_URL = os.getenv('TEST_DB_URL')

    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    JWT_EXPIRE_MIN: int = os.getenv('JWT_EXPIRE_MIN')
    JWT_SECRET: str = os.getenv('JWT_SECRET')

    MEDIA_DIR = BASE_DIR + '/media'

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


if not os.path.exists(settings.MEDIA_DIR):
    os.mkdir(settings.MEDIA_DIR)
