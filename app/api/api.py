from fastapi import APIRouter
from app.api.endpoints import users, users_images

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(users_images.router, prefix="/users", tags=["users-images"])