from pydantic import BaseModel


class Curso(BaseModel):
    id: int | None = None
    nome: str
    duracao: int
    valor: float
