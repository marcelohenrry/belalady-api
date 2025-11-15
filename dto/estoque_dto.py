from pydantic import BaseModel


class EstoqueDTO(BaseModel):
    id: int | None
    produto_id: int
    quantidade: float
    data_atualizacao: str | None