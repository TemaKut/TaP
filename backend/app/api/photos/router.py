from fastapi import APIRouter, Depends, File, UploadFile

from app.api.users.models import User
from app.api.users.source import get_current_user
from .schemas import PhotoGetSchema
from .crud import PhotosCRUD


photos_router = APIRouter(prefix='/photos', tags=['Фотографии'])


@photos_router.post('/upload')  # , response_model=PhotoGetSchema)
async def deploy_photo(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    crud: PhotosCRUD = Depends(),
):
    """ Добавить фотографию в БД. """
    await crud.upload_photo(file, user)

    return 1
