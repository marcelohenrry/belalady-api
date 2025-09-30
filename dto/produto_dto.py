from pydantic import BaseModel

from dto.categoria_dto import CategoriaDTO
from dto.marca_dto import MarcaDTO


class ProdutoDTO(BaseModel):
    id: int | None
    categoria: CategoriaDTO
    marca: MarcaDTO
    data_criacao: str | None
    descricao: str | None
    nome: str
    preco_base: float
    status: bool
