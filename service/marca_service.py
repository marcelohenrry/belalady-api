# service/marca_service.py
from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from dto.marca_dto import MarcaDTO
from modelo.marca import Marca


def salvar_marca(marca_dto: MarcaDTO, session: Session):
    try:
        print("Salvando marca:", marca_dto)
        marca = Marca(
            nome=marca_dto.nome,
            descricao=marca_dto.descricao,
            status=marca_dto.status,
            data_criacao=datetime.strptime(marca_dto.data_criacao,
                                           "%Y-%m-%d") if marca_dto.data_criacao else datetime.now()
        )
        session.add(marca)
        session.commit()
        session.refresh(marca)
        return marca
    except Exception as e:
        session.rollback()
        print("Erro ao salvar marca:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao salvar a informação da marca: {}".format(e)
        )


def atualizar(marca_id: int, marca_dto: MarcaDTO, session: Session):
    try:
        marca = session.get(Marca, marca_id)
        if not marca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marca não encontrada"
            )
        marca.nome = marca_dto.nome
        marca.descricao = marca_dto.descricao
        marca.status = marca_dto.status
        session.add(marca)
        session.commit()
        session.refresh(marca)
        return marca
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar marca:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar a informação da marca: {}".format(e)
        )


def listar(session: Session):
    try:
        marcas = session.exec(select(Marca)).all()
        print("Marcas encontradas:", marcas)
        marcas_dto = [
            MarcaDTO(
                id=m.id,
                nome=m.nome,
                descricao=m.descricao,
                status=m.status,
                data_criacao=m.data_criacao.strftime("%Y-%m-%d") if m.data_criacao else None
            )
            for m in marcas
        ]
        return marcas_dto
    except Exception as e:
        print("Erro ao listar marcas:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao listar marcas: {}".format(e)
        )
