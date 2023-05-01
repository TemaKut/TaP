from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    """ Базовая схема пользователя с общедоступными полями. """

    username: str


class UserCreateSchema(UserBaseSchema):
    """ Схема полей для создания пользователя. """

    password: str


class UserGetSchema(UserBaseSchema):
    """ Схема полей для получения данных пользователя в response. """

    id: int
    is_active: bool

    class Config:
        orm_mode = True


class TokenCreateSchema(BaseModel):
    """ Необходимые данные для получения токена пользователя. """

    username: str
    password: str


class TokenGetSchema(BaseModel):
    """ Схема представления токена в response. """

    token: str
    token_type: str = 'Bearer'
