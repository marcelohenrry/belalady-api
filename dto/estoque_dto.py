from pydantic import BaseModel


class EstoqueDTO(BaseModel):
    id: int | None
    produto_id: int
    quantidade: int
    data_atualizacao: str | None


class EstoqueCreateDTO(BaseModel):
    produto_id: int
    quantidade: int


class EstoqueUpdateDTO(BaseModel):
    quantidade: int | None = None


class AjusteEstoqueDTO(BaseModel):
    quantidade: int
    tipo_ajuste: str  # "entrada" ou "saida"
    observacao: str | None = None