from pydantic import BaseModel

from dto.endereco_dto import EnderecoDTO


class CategoriaDTO(BaseModel):
        id: int | None
        nome: str
        descricao: str | None
        status: bool
        data_criacao: str | None

