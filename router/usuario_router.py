from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from dto.cliente_dto import ClienteDTO
from dto.endereco_dto import EnderecoDTO
from modelo.usuario import Usuario
from resource.database import get_session
from service.usuario_sevice import salvar, atualizar

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuario_router.get("/", status_code=status.HTTP_200_OK)
async def get_clientes(session: Session = Depends(get_session)):
    usuarios = session.exec(select(Usuario)).all()
    clientes = []
    for usuario in usuarios:
        endereco = EnderecoDTO(**usuario.endereco.model_dump())
        print(f"Endereço encontrados: {endereco}")
        cliente = ClienteDTO(
            id=usuario.id,
            id_provedor=usuario.id_provedor,
            nome=usuario.nome,
            email=usuario.email,
            fone=usuario.fone,
            status=usuario.status,
            endereco=endereco
        )
        clientes.append(cliente)

    return clientes


@usuario_router.post("/", status_code=status.HTTP_201_CREATED)
async def salvar_cliente(cliente_dto: ClienteDTO, session: Session = Depends(get_session)):
    return salvar(cliente_dto, session)

@usuario_router.put("/{cliente_id}", status_code=status.HTTP_200_OK)
async def atualizar_cliente(cliente_id: int, cliente_dto: ClienteDTO, session: Session = Depends(get_session)):
    print(f"Atualizando cliente com ID: {cliente_id}")
    cliente_dto.id = cliente_id
    return atualizar(cliente_dto, session)