from pydantic import BaseModel

from dto.endereco_dto import EnderecoDTO


class ClienteDTO(BaseModel):
    id: int | None
    id_provedor: str | None
    nome: str
    email: str
    fone: str
    status: bool
    endereco: EnderecoDTO | None
