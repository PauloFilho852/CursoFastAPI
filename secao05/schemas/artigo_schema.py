from pydantic import BaseModel, ConfigDict


class ArtigoSchema(BaseModel):
    id: int | None = None
    titulo: str
    conteudo: str
    autor_id: int
    model_config: ConfigDict = ConfigDict(from_attributes=True)
