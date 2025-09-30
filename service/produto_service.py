from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from dto.produto_dto import ProdutoDTO
from modelo.produto import Produto


def salvar_produto(produto_dto: ProdutoDTO, session: Session):
    try:
        print("Salvando produto:", produto_dto)
        produto = Produto(
            nome=produto_dto.nome,
            descricao=produto_dto.descricao,
            status=produto_dto.status,
            data_criacao=datetime.strptime(produto_dto.data_criacao,
                                           "%Y-%m-%d") if produto_dto.data_criacao else datetime.now(),
            preco_base=produto_dto.preco_base,
            preco=produto_dto.preco_base,  # Ajuste conforme sua lógica de preço
            categoria_id=produto_dto.categoria.id,
            marca_id=produto_dto.marca.id
        )
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    except Exception as e:
        session.rollback()
        print("Erro ao salvar produto:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao salvar a informação do produto: {e}"
        )


def atualizar(produto_id: int, produto_dto: ProdutoDTO, session: Session):
    try:
        produto = session.get(Produto, produto_id)
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        produto.nome = produto_dto.nome
        produto.descricao = produto_dto.descricao
        produto.status = produto_dto.status
        produto.preco_base = produto_dto.preco_base
        produto.categoria_id = produto_dto.categoria.id
        produto.marca_id = produto_dto.marca.id
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar produto:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar a informação do produto: {e}"
        )


def listar(session: Session):
    try:
        produtos = session.exec(select(Produto)).all()
        print("Produtos encontrados:", produtos)
        produtos_dto = [
            ProdutoDTO(
                id=p.id,
                nome=p.nome,
                descricao=p.descricao,
                status=p.status,
                data_criacao=p.data_criacao.strftime("%Y-%m-%d") if p.data_criacao else None,
                preco_base=p.preco_base,
                categoria=p.categoria,
                marca=p.marca
            )
            for p in produtos
        ]
        return produtos_dto
    except Exception as e:
        print("Erro ao listar produtos:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao listar produtos: {e}"
        )


def listar_ativos(session: Session):
    try:
        produtos = session.exec(select(Produto).where(Produto.status == True)).all()
        produtos_dto = [
            ProdutoDTO(
                id=p.id,
                nome=p.nome,
                descricao=p.descricao,
                status=p.status,
                data_criacao=p.data_criacao.strftime("%Y-%m-%d") if p.data_criacao else None,
                preco_base=p.preco_base,
                categoria=p.categoria,
                marca=p.marca
            )
            for p in produtos
        ]
        return produtos_dto
    except Exception as e:
        print("Erro ao listar produtos ativos:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao listar produtos ativos: {e}"
        )
