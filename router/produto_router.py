from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dto.produto_dto import ProdutoDTO
from modelo.produto import Produto
from resource.database import get_session
from service.produto_service import salvar_produto, atualizar, listar, listar_ativos

produto_router = APIRouter(prefix="/produtos", tags=["produtos"])


@produto_router.post("/", response_model=Produto, status_code=status.HTTP_201_CREATED)
async def criar_produto(produto_dto: ProdutoDTO, session: Session = Depends(get_session)):
    produto = salvar_produto(produto_dto, session)
    return produto


@produto_router.put("/{produto_id}", response_model=Produto, status_code=status.HTTP_200_OK)
async def atualizar_produto(
        produto_id: int,
        produto_dto: ProdutoDTO,
        session: Session = Depends(get_session)
):
    print(f"Atualizando produto com ID: {produto_id}")
    produto = atualizar(produto_id, produto_dto, session)
    return produto


@produto_router.get("/", response_model=List[ProdutoDTO], status_code=status.HTTP_200_OK)
async def listar_produtos(session: Session = Depends(get_session)):
    produtos = listar(session)
    return produtos


@produto_router.get("/ativos", response_model=List[ProdutoDTO], status_code=status.HTTP_200_OK)
async def listar_produtos_ativos(session: Session = Depends(get_session)):
    produtos = listar_ativos(session)
    return produtos
