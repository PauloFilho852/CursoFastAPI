from fastapi import APIRouter
# from pydantic import BaseModel

router = APIRouter()


@router.get("/api/v1/cursos")
async def get_cursos():
    return {"cursos": ["Python", "Java", "JavaScript"]}
