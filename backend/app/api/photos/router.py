from fastapi import APIRouter, Depends, Body

from app.api.users.models import User
from app.api.users.source import get_current_user
from .schemas import PhotoCreate
from .crud import PhotosCRUD


photos_router = APIRouter(prefix='/photos', tags=['Photos'])


@photos_router.post('/deploy')
async def deploy_photo(
    photo_data: PhotoCreate = Body(),
    user: User = Depends(get_current_user),
    crud: PhotosCRUD = Depends(),
):
    """ Добавить фотографию в БД. """
    await crud.deploy_photo(photo_data, user)

    return 1
