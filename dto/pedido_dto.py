from datetime import datetime
from pydantic import BaseModel


class PedidoDTO(BaseModel):
    id: int | None = None
    data_atualizacao: datetime | None = None
    data_pedido: datetime | None = None
    status: str | None = None
    valor: float
    usuario_id: int
