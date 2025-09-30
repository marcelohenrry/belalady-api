from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from dto.categoria_dto import CategoriaDTO
from modelo.categoria import Categoria


def salvar_categoria(categoria_dto: CategoriaDTO, session: Session):
    try:
        print("Salvando categoria:", categoria_dto)
        categoria = Categoria(
            nome=categoria_dto.nome,
            descricao=categoria_dto.descricao,
            status=categoria_dto.status,
            data_criacao=datetime.strptime(categoria_dto.data_criacao,
                                           "%Y-%m-%d") if categoria_dto.data_criacao else datetime.now()
        )
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria
    except Exception as e:
        session.rollback()
        print("Erro ao salvar categoria:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao salvar a informação da categoria: {}".format(e)
        )


def atualizar(categoria_id: int, categoria_dto: CategoriaDTO, session: Session):
    try:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada"
            )
        categoria.nome = categoria_dto.nome
        categoria.descricao = categoria_dto.descricao
        categoria.status = categoria_dto.status
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar categoria:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar a informação da categoria: {}".format(e)
        )


def listar(session: Session):
    try:
        categorias = session.exec(select(Categoria)).all()
        print("Categorias encontradas:", categorias)
        categorias_dto = [
            CategoriaDTO(
                id=c.id,
                nome=c.nome,
                descricao=c.descricao,
                status=c.status,
                data_criacao=c.data_criacao.strftime("%Y-%m-%d") if c.data_criacao else None
            )
            for c in categorias
        ]
        return categorias_dto
    except Exception as e:
        print("Erro ao listar categorias:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao listar categorias: {}".format(e)
        )


def listar_ativas(session: Session):
    try:
        categorias = session.exec(
            select(Categoria).where(Categoria.status == True)
        ).all()
        categorias_dto = [
            CategoriaDTO(
                id=c.id,
                nome=c.nome,
                descricao=c.descricao,
                status=c.status,
                data_criacao=c.data_criacao.strftime("%Y-%m-%d") if c.data_criacao else None
            )
            for c in categorias
        ]
        return categorias_dto
    except Exception as e:
        print("Erro ao listar categorias ativas:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao listar categorias ativas: {e}"
        )
