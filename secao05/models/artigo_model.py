from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from .base_class import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_model import UserModel  # noqa: F401


class ArtigoModel(Base):
    __tablename__ = "artigos"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, index=True)
    titulo: Mapped[str] = Column(String(256), unique=True, index=True, nullable=False)
    conteudo: Mapped[str] = Column(String(256), nullable=False)
    autor_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    autor: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="artigos", lazy="joined"
    )
