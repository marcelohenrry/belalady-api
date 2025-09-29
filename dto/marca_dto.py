from pydantic import BaseModel


class MarcaDTO(BaseModel):
    id: int | None
    nome: str
    descricao: str | None
    status: bool
    data_criacao: str | None
