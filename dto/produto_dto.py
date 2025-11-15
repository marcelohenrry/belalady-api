from pydantic import BaseModel


class ProdutoDTO(BaseModel):
    id: int | None
    marca_id: int
    categoria_id: int
    data_criacao: str | None
    descricao: str | None
    nome: str
    preco_base: float
    status: bool
