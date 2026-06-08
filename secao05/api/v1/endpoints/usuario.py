from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import UserModel
from schemas.user_schema import UserSchema, CreateUserSchema
from core.database import get_async_session
from core.auth import pegar_usuario_atual, autenticar_usuario, criar_token_acesso
from core.security import gerar_hash_senha

DatabaseSession = Annotated[
    AsyncSession,
    Depends(get_async_session),
]
UsuarioAtual = Annotated[
    UserModel,
    Depends(pegar_usuario_atual),
]
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.post(
    "/signup",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def criar_usuario(
    usuario: CreateUserSchema,
    db: DatabaseSession,
) -> UserModel:
    usuario_existente = await db.execute(
        select(UserModel).where(UserModel.email == usuario.email)
    )
    usuario_existente = usuario_existente.scalars().first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )
    novo_usuario = UserModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        admin=usuario.admin,
        hashed_password=gerar_hash_senha(usuario.senha),
    )
    try:
        db.add(novo_usuario)
        await db.commit()
        await db.refresh(novo_usuario)
        return novo_usuario
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário",
        ) from e


@router.post(
    "/login",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def login_usuario(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DatabaseSession,
) -> JSONResponse:
    usuario = await autenticar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    token_acesso = criar_token_acesso({"sub": usuario.email})
    return JSONResponse(
        content={
            "access_token": token_acesso,
            "token_type": "bearer",
            "user": UserSchema.model_validate(usuario).model_dump(),
        },
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/",
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK,
)
async def listar_usuarios(
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> list[UserModel]:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas administradores podem listar usuários",
        )
    try:
        resultado = await db.execute(select(UserModel))
        usuarios = resultado.scalars().all()
        return usuarios
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar usuários",
        ) from e


@router.get(
    "/me",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def obter_usuario_atual(
    usuario: UsuarioAtual,
) -> UserModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    return usuario


@router.get(
    "/{usuario_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def obter_usuario_por_id(
    usuario_id: int,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> UserModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas administradores podem acessar outros usuários",
        )
    try:
        resultado = await db.execute(
            select(UserModel).where(UserModel.id == usuario_id)
        )
        usuario_encontrado = resultado.scalars().first()
        if not usuario_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return usuario_encontrado
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter usuário",
        ) from e


@router.put("/me", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def atualizar_usuario_atual(
    usuario_atualizado: CreateUserSchema, db: DatabaseSession, usuario: UsuarioAtual
) -> UserModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    usuario.nome = usuario_atualizado.nome
    usuario.sobrenome = usuario_atualizado.sobrenome
    usuario.email = usuario_atualizado.email
    usuario.admin = usuario_atualizado.admin
    usuario.senha_hash = gerar_hash_senha(usuario_atualizado.senha)

    try:
        db.add(usuario)
        await db.commit()
        await db.refresh(usuario)
        return usuario

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar usuário",
        ) from e


@router.put(
    "/{usuario_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def atualizar_usuario(
    usuario_id: int,
    usuario_atualizado: CreateUserSchema,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> UserModel:
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas administradores podem atualizar outros usuários",
        )
    try:
        resultado = await db.execute(
            select(UserModel).where(UserModel.id == usuario_id)
        )
        usuario_encontrado = resultado.scalars().first()
        if not usuario_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        usuario_encontrado.nome = usuario_atualizado.nome
        usuario_encontrado.sobrenome = usuario_atualizado.sobrenome
        usuario_encontrado.email = usuario_atualizado.email
        usuario_encontrado.admin = usuario_atualizado.admin
        usuario_encontrado.senha_hash = gerar_hash_senha(usuario_atualizado.senha)
        db.add(usuario_encontrado)
        await db.commit()
        await db.refresh(usuario_encontrado)
        return usuario_encontrado
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar usuário",
        ) from e


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deletar_usuario_atual(
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> Response:

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    try:
        await db.delete(usuario)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar usuário",
        ) from e


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deletar_usuario(
    usuario_id: int,
    db: DatabaseSession,
    usuario: UsuarioAtual,
) -> Response:

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas administradores podem deletar outros usuários",
        )
    try:
        resultado = await db.execute(
            select(UserModel).where(UserModel.id == usuario_id)
        )
        usuario_encontrado = resultado.scalars().one_or_none()
        if not usuario_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        await db.delete(usuario_encontrado)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar usuário",
        ) from e
