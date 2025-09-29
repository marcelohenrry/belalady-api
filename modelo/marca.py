from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

class Marca(SQLModel, table=True):
    __tablename__ = "marca"

    id: int = Field(primary_key=True)
    nome: str
    descricao: Optional[str]
    status: bool
    data_criacao: datetime
