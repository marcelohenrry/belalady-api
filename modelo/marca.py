from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Marca(SQLModel, table=True):
    __tablename__ = "marca"

    id: int = Field(primary_key=True)
    nome: str = Field(max_length=100, unique=True)
    descricao: Optional[str] = None
    status: bool
    data_criacao: datetime