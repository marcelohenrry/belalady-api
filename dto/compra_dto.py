from pydantic import BaseModel

from dto.cliente_dto import ClienteDTO


class CompraDTO(BaseModel):
    id: int | None
    data_atualizacao: str | None
    data_pedido: str | None
    status: str | None
    valor: float
    usuario: ClienteDTO
