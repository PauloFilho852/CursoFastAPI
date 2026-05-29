from pydantic import BaseModel as SChemaBaseModel

class CursoSchema(SChemaBaseModel):
    id: int | None
    nome: str
    descricao: str
    duracao: int

    class Config:
        orm_mode = True