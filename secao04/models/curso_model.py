from core.settings import settings
from sqlalchemy import Column, Integer, String

class CursoModel(settings.DBBaseModel):
    __tablename__ = 'cursos'

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(255), nullable=False)
    descricao: str = Column(String(255), nullable=False)