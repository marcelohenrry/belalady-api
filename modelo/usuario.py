from typing import Optional, TYPE_CHECKING

from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from model.endereco import Endereco


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: int = Field(primary_key=True)
    id_provedor: Optional[str]
    nome: str
    email: Optional[str]
    fone: str
    status: bool

    endereco: Optional["Endereco"] = Relationship(back_populates="usuario")
