from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dto.estoque_dto import EstoqueDTO, EstoqueCreateDTO, EstoqueUpdateDTO, AjusteEstoqueDTO
from modelo.estoque import Estoque
from resource.database import get_session
from service.estoque_service import (
    salvar_estoque, atualizar, listar, buscar_por_id,
    buscar_por_produto, ajustar_estoque, deletar
)

estoque_router = APIRouter(prefix="/estoques", tags=["estoques"])


@estoque_router.post("/", response_model=Estoque, status_code=status.HTTP_201_CREATED)
async def criar_estoque(estoque_dto: EstoqueCreateDTO, session: Session = Depends(get_session)):
    estoque = salvar_estoque(estoque_dto, session)
    return estoque


@estoque_router.put("/{estoque_id}", response_model=Estoque, status_code=status.HTTP_200_OK)
async def atualizar_estoque(
        estoque_id: int,
        estoque_dto: EstoqueUpdateDTO,
        session: Session = Depends(get_session)
):
    print(f"Atualizando estoque com ID: {estoque_id}")
    estoque = atualizar(estoque_id, estoque_dto, session)
    return estoque


@estoque_router.post("/produto/{produto_id}/ajustar", response_model=Estoque, status_code=status.HTTP_200_OK)
async def ajustar_estoque_produto(
        produto_id: int,
        ajuste_dto: AjusteEstoqueDTO,
        session: Session = Depends(get_session)
):
    print(f"Ajustando estoque do produto ID: {produto_id}")
    estoque = ajustar_estoque(produto_id, ajuste_dto, session)
    return estoque


@estoque_router.get("/", response_model=List[EstoqueDTO], status_code=status.HTTP_200_OK)
async def listar_estoques(session: Session = Depends(get_session)):
    estoques = listar(session)
    return estoques


@estoque_router.get("/{estoque_id}", response_model=EstoqueDTO, status_code=status.HTTP_200_OK)
async def buscar_estoque(estoque_id: int, session: Session = Depends(get_session)):
    estoque = buscar_por_id(estoque_id, session)
    return estoque


@estoque_router.get("/produto/{produto_id}", response_model=EstoqueDTO, status_code=status.HTTP_200_OK)
async def buscar_estoque_por_produto(produto_id: int, session: Session = Depends(get_session)):
    estoque = buscar_por_produto(produto_id, session)
    return estoque


@estoque_router.delete("/{estoque_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_estoque(estoque_id: int, session: Session = Depends(get_session)):
    deletar(estoque_id, session)
    return None