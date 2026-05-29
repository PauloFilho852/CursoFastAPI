from pydantic import BaseModel, field_validator


class Curso(BaseModel):
    id: int | None = None
    nome: str
    duracao: int
    valor: float

    @field_validator("nome")
    def validar_nome(cls, value):
        if len(value) < 3:
            raise ValueError("O nome do curso deve conter pelo menos 3 caracteres.")
        return value
