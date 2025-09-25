from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    id: int = Field(primary_key=True)
    nome: str
    descricao: Optional[str]
    status: bool
    data_criacao: datetime
