from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Estoque(SQLModel, table=True):
    __tablename__ = "estoque"

    id: int = Field(primary_key=True)
    produto_id: int = Field(foreign_key="produto.id", unique=True)
    quantidade: int
    data_atualizacao: datetime = Field(description="Última modificação")