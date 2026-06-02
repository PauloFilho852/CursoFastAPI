from pydantic import BaseModel as SChemaBaseModel, ConfigDict


class CursoSchema(SChemaBaseModel):
    id: int | None = None
    nome: str
    descricao: str
    duracao: int
    model_config: ConfigDict = ConfigDict(from_attributes=True)
