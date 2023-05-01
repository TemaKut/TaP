import sqlalchemy as sa
from passlib.hash import bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from fastapi import HTTPException, status

from app.database.base import Base
from app.settings import log


class User(Base):
    """ Модель БД. Пользователь. """
    __tablename__ = 'users'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        comment='Id пользователя',
    )
    username = sa.Column(
        sa.String(50),
        unique=True,
        nullable=False,
        comment='Псеводним',
    )
    password = sa.Column(
        sa.Text,
        nullable=False,
        comment='Хэш пароля',
    )
    registred_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment='Дата и время регистрации пользователя.',
    )
    is_active = sa.Column(
        sa.Boolean,
        nullable=False,
        default=True,
        comment='Флаг активен ли пользователь.',
    )

    @validates('password')
    def password_validate(self, key, value):
        """ Хэширование пароля. """

        return bcrypt.hash(value)

    def verify_password(self, password: str) -> bool:
        """ Верифицирование пароля. """
        if not bcrypt.verify(password, self.password):
            log.error('Incorrect password')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect password',
            )

        return True

    def __repr__(self):
        """ Строчное представление объекта. """

        return f'{self.__class__.__name__}<id={self.id}>'
