from pydantic import BaseModel


class EnderecoDTO(BaseModel):
        id: int | None
        bairro: str
        cep: str
        cidade: str
        complemento: str | None
        logradouro: str
        numero: str | None
