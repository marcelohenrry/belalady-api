from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dto.compra_dto import CompraDTO
from dto.pedido_dto import PedidoDTO
from resource.database import get_session
from service.pedido_service import (
    salvar_pedido,
    atualizar_pedido,
    listar_pedidos,
    buscar_pedido_por_id
)

pedido_router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@pedido_router.post("/", response_model=PedidoDTO, status_code=status.HTTP_201_CREATED)
async def criar_pedido(pedido_dto: PedidoDTO, session: Session = Depends(get_session)):
    pedido = salvar_pedido(pedido_dto, session)
    return PedidoDTO.model_validate(pedido.__dict__)


@pedido_router.put("/{pedido_id}", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def atualizar_pedido_router(
        pedido_id: int,
        pedido_dto: PedidoDTO,
        session: Session = Depends(get_session)
):
    pedido = atualizar_pedido(pedido_id, pedido_dto, session)
    return PedidoDTO.model_validate(pedido.__dict__)


@pedido_router.get("/", response_model=List[CompraDTO], status_code=status.HTTP_200_OK)
async def listar_todos_pedidos(session: Session = Depends(get_session)):
    return listar_pedidos(session)


@pedido_router.get("/{pedido_id}", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def buscar_pedido(pedido_id: int, session: Session = Depends(get_session)):
    return buscar_pedido_por_id(pedido_id, session)
