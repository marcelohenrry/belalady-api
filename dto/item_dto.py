from pydantic import BaseModel


class ItemDTO(BaseModel):
    id: int | None
    quantidade: int
    produto_id: int | None
    pedido_id: int | None
    data_criacao: str | None
