from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    __tablename__ = "item"

    id: int = Field(primary_key=True)
    quantidade: int

    pedido_id: int = Field(foreign_key="pedido.id")
    produto_id: int = Field(foreign_key="produto.id")

    data_criacao: Optional[datetime]
