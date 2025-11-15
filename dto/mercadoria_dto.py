from typing import Optional

from pydantic import BaseModel

from dto.categoria_dto import CategoriaDTO
from dto.marca_dto import MarcaDTO


class MercadoriaDTO(BaseModel):
    id: int | None
    categoria: Optional[CategoriaDTO] | None
    marca: Optional[MarcaDTO] | None
    data_criacao: str | None
    descricao: str | None
    nome: str
    preco_base: float
    status: bool
