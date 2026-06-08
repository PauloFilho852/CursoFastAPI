from fastapi import APIRouter
from .endpoints import usuario, artigo

api_routers = APIRouter()
api_routers.include_router(usuario.router)
api_routers.include_router(artigo.router)
