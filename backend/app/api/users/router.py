from fastapi import APIRouter, Depends, Body, status

from . import bad_responses as br
from .models import User
from .crud import UsersCRUD
from .source import get_current_user
from .schemas import (
    UserCreateSchema,
    UserGetSchema,
    TokenCreateSchema,
    TokenGetSchema,
)


users_router = APIRouter(prefix='/users', tags=['Пользователи'])


@users_router.post(
    '/get-token',
    name='get-token',
    response_model=TokenGetSchema,
    responses={
        404: {'model': br.UserNotFound}
    }
)
async def get_token(
    data: TokenCreateSchema = Body(),
    crud: UsersCRUD = Depends(),
):
    """ Получить jwt токен для пользователя. """
    token = await crud.create_token(data)

    return token


@users_router.post(
    '/',
    name='create_user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserGetSchema,
    responses={
        400: {'model': br.UserAlredyExists},
        500: {'model': br.UserAddInDbError},
    }
)
async def create_user(
    data: UserCreateSchema = Body(),
    crud: UsersCRUD = Depends(),
):
    """ Создать пользователя. """
    user = await crud.create_user(data)

    return user


@users_router.get(
    '/',
    name='get_list_of_users',
    response_model=list[UserGetSchema],
)
async def get_list_of_users(crud: UsersCRUD = Depends()):
    """ Получить список всех пользователей. """
    users = await crud.get_list_of_users()

    return users


@users_router.get(
    '/me',
    name='get_info_about_me',
    response_model=UserGetSchema,
    responses={
        401: {'model': br.AuthenticationRequired}
    }
)
async def get_info_about_me(user: User = Depends(get_current_user)):
    """ Вернуть информацию о пользователе. """

    return user


@users_router.get(
    '/{username}',
    name='get_user_by_username',
    response_model=UserGetSchema,
)
async def get_user_by_username(
    username: str,
    crud: UsersCRUD = Depends(),
):
    """ Получить пользлователя по username. """
    user = await crud.get_user_from_db(username)

    return user
