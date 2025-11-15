from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship

from modelo.categoria import Categoria
from modelo.marca import Marca


class Produto(SQLModel, table=True):
    __tablename__ = "produto"

    id: int = Field(primary_key=True)
    nome: str
    descricao: Optional[str]
    status: bool
    data_criacao: datetime
    preco_base: float

    marca_id: int = Field(foreign_key="marca.id")
    marca: Mapped["Marca"] = Relationship(back_populates="produto")

    categoria_id: int = Field(foreign_key="categoria.id")
    categoria: Mapped["Categoria"] = Relationship(back_populates="produto")