from fastapi import APIRouter, Depends, File, UploadFile, Form

from app.api.users.models import User
from app.api.users.source import get_current_user
from .schemas import PhotoGetSchema, PhotoCreate
from .crud import PhotosCRUD


photos_router = APIRouter(prefix='/photos', tags=['Фотографии'])


@photos_router.post('/upload')  # , response_model=PhotoGetSchema)
async def deploy_photo(
    photo_data: PhotoCreate = Depends(),
    file: UploadFile = File(),
    # user: User = Depends(get_current_user),
    crud: PhotosCRUD = Depends(),
):
    """ Добавить фотографию в БД. """
    print(photo_data)
    # uri = await crud.upload_photo(file, user)

    return 1
