from fastapi import APIRouter

from .users.router import users_router
from .photos.router import photos_router


api_router = APIRouter(prefix='/api/v1')

api_router.include_router(users_router)
api_router.include_router(photos_router)
