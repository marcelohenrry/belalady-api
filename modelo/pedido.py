from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship

from modelo.usuario import Usuario


class Pedido(SQLModel, table=True):
    __tablename__ = "pedido"

    id: int = Field(primary_key=True)

    data_atualizacao: datetime
    data_pedido: datetime
    status: str = Field(default="Pendente")
    valor: float

    usuario_id: int | None = Field(foreign_key="usuario.id")
    usuario: Mapped["Usuario"] = Relationship(back_populates="pedido")
