from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dto.marca_dto import MarcaDTO, MarcaCreateDTO, MarcaUpdateDTO
from modelo.marca import Marca
from resource.database import get_session
from service.marca_service import salvar_marca, atualizar, listar, buscar_por_id, deletar

marca_router = APIRouter(prefix="/marcas", tags=["marcas"])


@marca_router.post("/", response_model=Marca, status_code=status.HTTP_201_CREATED)
async def criar_marca(marca_dto: MarcaCreateDTO, session: Session = Depends(get_session)):
    marca = salvar_marca(marca_dto, session)
    return marca


@marca_router.put("/{marca_id}", response_model=Marca, status_code=status.HTTP_200_OK)
async def atualizar_marca(
        marca_id: int,
        marca_dto: MarcaUpdateDTO,
        session: Session = Depends(get_session)
):
    print(f"Atualizando marca com ID: {marca_id}")
    marca = atualizar(marca_id, marca_dto, session)
    return marca


@marca_router.get("/", response_model=List[MarcaDTO], status_code=status.HTTP_200_OK)
async def listar_marcas(session: Session = Depends(get_session)):
    marcas = listar(session)
    return marcas


@marca_router.get("/{marca_id}", response_model=MarcaDTO, status_code=status.HTTP_200_OK)
async def buscar_marca(marca_id: int, session: Session = Depends(get_session)):
    marca = buscar_por_id(marca_id, session)
    return marca


@marca_router.delete("/{marca_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_marca(marca_id: int, session: Session = Depends(get_session)):
    deletar(marca_id, session)
    return None