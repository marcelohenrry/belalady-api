from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dto.cliente_dto import ClienteDTO
from model.usuario import Usuario
from resource.database import get_session

usuario_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuario_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Usuario])
async def get_clientes(session: Session = Depends(get_session())):
    clientes = session.exec(select(Usuario)).all()
    return clientes


@usuario_router.post("/", status_code=status.HTTP_201_CREATED)
async def salvar_cliente(cliente_dto: ClienteDTO, session: Session = Depends(criar_sessao)):
    try:
        endereco = Endereco(cliente_dto.endereco)
        print(f"Cliente {cliente_dto}")
        session.add(Cliente(cliente_dto))

        print(f"Cliente salvo: {cliente_dto}")

        endereco.usuario_id = cliente_dto.id
        session.add(Endereco(endereco))
        session.commit()

        print(f"Endereço salvo: {endereco}")

        return {"message": "Cliente salvo com sucesso"}
    except Exception as e:
        print("Erro ao salvar cliente:", e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao salvar a informação do cliente: {}".format(e)
        )
