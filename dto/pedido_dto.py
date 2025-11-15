from pydantic import BaseModel


class PedidoDTO(BaseModel):
    id: int | None
    data_atualizacao: str | None
    data_pedido: str | None
    status: str | None
    valor: float
    usuario_id: int
