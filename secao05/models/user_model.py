from sqlalchemy import Column, Integer, String
from .base_class import Base
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .artigo_model import ArtigoModel


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = Column(String(256), unique=True, index=True, nullable=False)
    nome: Mapped[str] = Column(String(256), nullable=False)
    sobrenome: Mapped[str] = Column(String(256), nullable=False)
    admin: Mapped[int] = Column(Integer, default=0, nullable=False)
    hashed_password: Mapped[str] = Column(String(256), nullable=False)
    artigos: Mapped[list["ArtigoModel"]] = relationship(
        "ArtigoModel",
        cascade="all, delete-orphan",
        back_populates="autor",
        uselist=True,
    )
