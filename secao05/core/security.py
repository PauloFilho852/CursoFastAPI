from passlib.context import CryptContext

CRIPT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return CRIPT_CONTEXT.verify(senha, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    return CRIPT_CONTEXT.hash(senha)