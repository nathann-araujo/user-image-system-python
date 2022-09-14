from fastapi import APIRouter
from app.api.endpoints import routes


api_router = APIRouter()
api_router.include_router(routes.router, tags=["api"])
