from typing import Optional

from pydantic import BaseModel

from dto.mercadoria_dto import MercadoriaDTO


class ArmazenamentoDTO(BaseModel):
    id: int | None
    produto: Optional[MercadoriaDTO] | None
    quantidade: float
    data_atualizacao: str | None
