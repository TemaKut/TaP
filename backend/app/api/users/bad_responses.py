from pydantic import BaseModel


class UserNotFound(BaseModel):
    """ Bad response. Пользователь не найден в БД. """

    description: str = 'User not found.'


class UserAlredyExists(BaseModel):
    """ Bad response. Пользователь ужесуществует в БД. """

    description: str = 'User alredy exists.'


class UserAddInDbError(BaseModel):
    """ Bad response. Ошибка добавления пользователя в БД. """

    description: str = 'Error with add user in DB'


class AuthenticationRequired(BaseModel):
    """ Bad response. Необходима передача токена авторизации.. """

    description: str = 'Authorization required.'
