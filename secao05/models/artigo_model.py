from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base_class import Base

class ArtigoModel(Base):
    __tablename__ = "artigos"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column(String(256), unique=True, index=True, nullable=False)
    conteudo = Column(String(256), nullable=False)
    autor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    autor = relationship("UserModel", back_populates="artigos", lazy="joined")
