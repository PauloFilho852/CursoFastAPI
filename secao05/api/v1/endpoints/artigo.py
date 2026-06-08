from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.artigo_model import ArtigoModel
from models.user_model import UserModel
from schemas.artigo_schema import ArtigoSchema
from core.database import get_async_session
from core.auth import pegar_usuario_atual

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_async_session),
]
UsuarioAtual = Annotated[
    UserModel,
    Depends(pegar_usuario_atual),
]
router = APIRouter(
    prefix="/artigos",
    tags=["artigos"],
)


@router.post(
    "/",
    response_model=ArtigoSchema,
    status_code=status.HTTP_201_CREATED,
)
async def criar_artigo(
    artigo: ArtigoSchema,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> ArtigoModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado.",
        )
    novo_artigo = ArtigoModel(
        titulo=artigo.titulo,
        conteudo=artigo.conteudo,
        autor_id=usuario.id,
    )
    try:
        db.add(novo_artigo)
        await db.commit()
        await db.refresh(novo_artigo)
        return novo_artigo
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar artigo.",
        ) from e


@router.get("/", response_model=list[ArtigoSchema], status_code=status.HTTP_200_OK)
async def listar_artigos(
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> list[ArtigoModel]:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado.",
        )
    try:
        result = await db.execute(
            select(ArtigoModel).where(ArtigoModel.autor_id == usuario.id)
        )
        artigos = result.scalars().all()
        if not artigos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum artigo encontrado.",
            )
        return artigos
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar artigos.",
        ) from e


@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def obter_artigo(
    artigo_id: int,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> ArtigoModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado.",
        )
    try:
        result = await db.execute(
            select(ArtigoModel).where(ArtigoModel.id == artigo_id)
        )
        artigo = result.scalars().one_or_none()
        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado.",
            )
        if artigo.autor_id != usuario.id and not usuario.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não autorizado a acessar este artigo.",
            )
        return artigo
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter artigo.",
        ) from e


@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def atualizar_artigo(
    artigo_id: int,
    artigo_atualizado: ArtigoSchema,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> ArtigoModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado.",
        )
    try:
        result = await db.execute(
            select(ArtigoModel).where(ArtigoModel.id == artigo_id)
        )
        artigo = result.scalars().one_or_none()
        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado.",
            )
        if artigo.autor_id != usuario.id and not usuario.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não autorizado a atualizar este artigo.",
            )
        artigo.titulo = artigo_atualizado.titulo
        artigo.conteudo = artigo_atualizado.conteudo
        await db.commit()
        await db.refresh(artigo)
        return artigo
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar artigo.",
        ) from e


@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_artigo(
    artigo_id: int,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> None:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado.",
        )
    try:
        result = await db.execute(
            select(ArtigoModel).where(ArtigoModel.id == artigo_id)
        )
        artigo = result.scalars().one_or_none()
        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado.",
            )
        if artigo.autor_id != usuario.id and not usuario.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não autorizado a deletar este artigo.",
            )
        await db.delete(artigo)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar artigo.",
        ) from e
