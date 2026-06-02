from pytz import timezone
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from .settings import settings
from .security import verificar_senha, gerar_hash_senha
from .database import get_async_session
from models.user_model import UserModel as User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")

async def autenticar_usuario(email: str, senha: str) -> User:
    async with get_async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user or not verificar_senha(senha, user.hashed_password):
            return None
        return user
    
def criar_token_acesso(payload: dict, expires_delta: timedelta = None) -> str:
    payload_to_encode = payload.copy()
    
    if expires_delta:
        expire = datetime.now(timezone('America/Sao_Paulo')) + expires_delta
    else:        
        expire = datetime.now(timezone('America/Sao_Paulo')) + timedelta(minutes=15)

    payload_to_encode.update({"exp": expire})    
    encoded_jwt = jwt.encode(payload_to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def pegar_usuario_atual(token: str = oauth2_scheme) -> User:
    credentials_exception = JWTError("Não foi possível validar as credenciais")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    async with get_async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user is None:
            raise credentials_exception
        return user