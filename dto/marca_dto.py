from pydantic import BaseModel


class MarcaDTO(BaseModel):
    id: int | None
    nome: str
    descricao: str | None
    status: bool
    data_criacao: str | None


class MarcaCreateDTO(BaseModel):
    nome: str
    descricao: str | None = None
    status: bool = True


class MarcaUpdateDTO(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    status: bool | None = None