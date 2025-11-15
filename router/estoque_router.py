from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dto.estoque_dto import EstoqueDTO
from dto.armazenamento_dto import ArmazenamentoDTO
from modelo.estoque import Estoque
from resource.database import get_session
from service.estoque_service import salvar_estoque, atualizar_estoque, listar_estoque

estoque_router = APIRouter(prefix="/estoques", tags=["estoques"])

@estoque_router.post("/", response_model=Estoque, status_code=status.HTTP_201_CREATED)
async def criar_estoque(estoque_dto: EstoqueDTO, session: Session = Depends(get_session)):
    return salvar_estoque(estoque_dto, session)

@estoque_router.put("/{estoque_id}", response_model=Estoque, status_code=status.HTTP_200_OK)
async def atualizar_estoque_endpoint(estoque_id: int, estoque_dto: EstoqueDTO, session: Session = Depends(get_session)):
    return atualizar_estoque(estoque_id, estoque_dto, session)

@estoque_router.get("/", response_model=List[ArmazenamentoDTO], status_code=status.HTTP_200_OK)
async def listar_estoques(session: Session = Depends(get_session)):
    return listar_estoque(session)
