from typing import Optional

from sqlalchemy.orm import Mapped
from sqlmodel import Relationship, SQLModel, Field


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: int = Field(primary_key=True)
    id_provedor: Optional[str]
    nome: str
    email: Optional[str]
    fone: str
    status: bool

    endereco: Mapped["Endereco"] = Relationship(back_populates="usuario")

class Endereco(SQLModel, table=True):
    __tablename__ = "endereco"

    id: int = Field(primary_key=True)
    bairro: str
    cep: str
    cidade: str
    complemento: Optional[str]
    logradouro: str
    numero: str

    usuario_id: int | None = Field(foreign_key="usuario.id")
    usuario: Mapped["Usuario"] = Relationship(back_populates="endereco")
