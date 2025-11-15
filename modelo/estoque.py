from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship

from modelo.produto import Produto

class Estoque(SQLModel, table=True):
    __tablename__ = "estoque"

    id: int = Field(primary_key=True)
    produto_id: int = Field(foreign_key="produto.id")
    produto: Mapped["Produto"] = Relationship()
    quantidade: float
    data_atualizacao: Optional[datetime]