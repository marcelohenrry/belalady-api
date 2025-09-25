from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dto.categoria_dto import CategoriaDTO
from modelo.categoria import Categoria
from resource.database import get_session
from service.categoria_service import salvar_categoria, atualizar, listar

categoria_router = APIRouter(prefix="/categorias", tags=["categorias"])


@categoria_router.post("/", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def criar_categoria(categoria_dto: CategoriaDTO, session: Session = Depends(get_session)):
    categoria = salvar_categoria(categoria_dto, session)
    return categoria


@categoria_router.put("/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def atualizar_categoria(
        categoria_id: int,
        categoria_dto: CategoriaDTO,
        session: Session = Depends(get_session)
):
    print(f"Atualizando categoria com ID: {categoria_id}")
    categoria = atualizar(categoria_id, categoria_dto, session)
    return categoria


@categoria_router.get("/", response_model=List[CategoriaDTO], status_code=status.HTTP_200_OK)
async def listar_categorias(session: Session = Depends(get_session)):
    categorias = listar(session)
    return categorias
