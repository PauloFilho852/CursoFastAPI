from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_async_session
from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.post("/", response_model=CursoSchema, status_code=status.HTTP_201_CREATED)
async def criar_curso(
    curso: CursoSchema, session: AsyncSession = Depends(get_async_session)
):
    novo_curso = CursoModel(
        nome=curso.nome, descricao=curso.descricao, duracao=curso.duracao
    )
    session.add(novo_curso)
    await session.commit()
    await session.refresh(novo_curso)
    return novo_curso


@router.get("/", response_model=list[CursoSchema])
async def obter_curso(session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: list[CursoModel] = result.scalars().all()
    return cursos


@router.get("/{curso_id}", response_model=CursoSchema)
async def obter_curso_por_id(
    curso_id: int, session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        query = select(CursoModel).where(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel | None = result.scalar_one_or_none()
    if curso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
        )
    return curso


@router.put(
    "/{curso_id}", response_model=CursoSchema, status_code=status.HTTP_202_ACCEPTED
)
async def atualizar_curso(
    curso_id: int,
    curso_atualizado: CursoSchema,
    session: AsyncSession = Depends(get_async_session),
):
    async with session.begin():
        query = select(CursoModel).where(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel | None = result.scalar_one_or_none()
        if curso is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
            )
        curso.nome = curso_atualizado.nome
        curso.descricao = curso_atualizado.descricao
        curso.duracao = curso_atualizado.duracao

    await session.refresh(curso)

    return curso


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_curso(
    curso_id: int, session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        query = select(CursoModel).where(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel | None = result.scalar_one_or_none()
        if curso is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado"
            )
        await session.delete(curso)
        await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
