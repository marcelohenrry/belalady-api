from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Produto(SQLModel, table=True):
    __tablename__ = "produto"

    id: int = Field(primary_key=True)
    nome: str
    descricao: Optional[str]
    preco: float
    status: bool
    data_criacao: datetime
    preco_base: float

    marca_id: int = Field(foreign_key="marca.id")
    categoria_id: int = Field(foreign_key="categoria.id")
