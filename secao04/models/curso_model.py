from models.base_class import Base
from sqlalchemy import Column, Integer, String


class CursoModel(Base):
    __tablename__ = "cursos"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome: str = Column(String(255), nullable=False)
    descricao: str = Column(String(255), nullable=False)
    duracao: int = Column(Integer, nullable=False)
