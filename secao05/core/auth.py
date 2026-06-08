from typing import Annotated
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pytz import timezone
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from .settings import settings
from .security import verificar_senha
from .database import get_async_session
from models.user_model import UserModel as User
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://127.0.0.1:8000/api/v1/usuarios/login"
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possível validar as credenciais",
    headers={"WWW-Authenticate": "Bearer"},
)


async def _autenticar_usuario(
    email: str, senha: str, session: AsyncSession
) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user: User | None = result.scalars().one_or_none()
    if not user or not verificar_senha(senha, user.hashed_password):
        return None
        return user


async def autenticar_usuario(email: str, senha: str, session: AsyncSession):

    print("EMAIL RECEBIDO:", repr(email))
    print("SENHA RECEBIDA:", repr(senha))

    result = await session.execute(select(User).where(User.email == email))

    user = result.scalars().one_or_none()

    print("USUARIO:", user)

    if user:
        print("HASH:", user.hashed_password)

        resultado = verificar_senha(senha, user.hashed_password)

        print("VERIFY:", resultado)

    return user


def criar_token_acesso(payload: dict, expires_delta: timedelta = None) -> str:
    payload_to_encode = payload.copy()

    if expires_delta:
        expire = datetime.now(timezone("America/Sao_Paulo")) + expires_delta
    else:
        expire = datetime.now(timezone("America/Sao_Paulo")) + timedelta(minutes=15)

    payload_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload_to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def pegar_usuario_atual(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        email: str | None = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await session.execute(select(User).where(User.email == email))

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
