from fastapi import APIRouter
# from pydantic import BaseModel

router = APIRouter()


@router.get("/api/v1/usuarios")
async def get_usuarios():
    return {"usuarios": ["Alice", "Bob", "Charlie"]}
