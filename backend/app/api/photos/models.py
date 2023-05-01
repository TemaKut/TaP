import sqlalchemy as sa
from sqlalchemy.sql import func

from app.database.base import Base
from app.api.users.models import User


class Photo(Base):
    """ Модель фотографии """
    __tablename__ = 'photos'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        comment='Идентификатор в БД',
    )
    image_uri = sa.Column(
        sa.Text,
        nullable=False,
        comment='Ссылка на доступ к фотографии.',
    )
    owner_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id),
        nullable=False,
        comment='Владелец фотограции. (User)'
    )
    description = sa.Column(
        sa.String(300),
        nullable=True,
        comment='Текстовое описание фотографии.',
    )
    added_at = sa.Column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def __repr__(self):
        """ Строчное представление объекта. """

        return f'{self.__class__.__name__}<{self.id=}, {self.image_url=}>'
