from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship


class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    id: int = Field(primary_key=True)
    nome: str
    descricao: Optional[str]
    status: bool
    data_criacao: datetime

    produto: Mapped[List["Produto"]] = Relationship(back_populates="categoria")
