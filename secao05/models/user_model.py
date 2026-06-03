from sqlalchemy import Column, Integer, String
from .base_class import Base
from sqlalchemy.orm import relationship
from .artigo_model import ArtigoModel  # noqa: F401


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    nome = Column(String(256), nullable=False)
    sobrenome = Column(String(256), nullable=False)
    admin = Column(Integer, default=0, nullable=False)
    hashed_password = Column(String, nullable=False)
    artigos = relationship(
        "ArtigoModel",
        cascade="all, delete-orphan",
        back_populates="autor",
        uselist=True,
        lazy="joined",
    )
