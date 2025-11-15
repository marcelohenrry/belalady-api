from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from dto.armazenamento_dto import ArmazenamentoDTO
from dto.estoque_dto import EstoqueDTO
from dto.mercadoria_dto import MercadoriaDTO
from modelo.estoque import Estoque


def salvar_estoque(estoque_dto: EstoqueDTO, session: Session):
    try:
        estoque = session.exec(select(Estoque).where(Estoque.produto_id == estoque_dto.produto_id)).first()
        if estoque:
            raise HTTPException(status_code=209, detail="Estoque já existe para este produto")
        estoque = Estoque(
            produto_id=estoque_dto.produto_id,
            quantidade=estoque_dto.quantidade,
            data_atualizacao=datetime.strptime(estoque_dto.data_atualizacao,
                                               "%Y-%m-%d") if estoque_dto.data_atualizacao else datetime.now()
        )
        session.add(estoque)
        session.commit()
        session.refresh(estoque)
        return estoque
    except Exception as e:
        print("Erro ao salvar estoque:", e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao salvar estoque: {e}"
        )


def atualizar_estoque(estoque_id: int, estoque_dto: EstoqueDTO, session: Session):
    try:
        estoque = session.get(Estoque, estoque_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado"
            )
        estoque.produto_id = estoque_dto.produto_id
        estoque.quantidade = estoque_dto.quantidade
        estoque.data_atualizacao = datetime.strptime(estoque_dto.data_atualizacao,
                                                     "%Y-%m-%d") if estoque_dto.data_atualizacao else datetime.now()
        session.add(estoque)
        session.commit()
        session.refresh(estoque)
        return estoque
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar estoque:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar estoque: {e}"
        )


def listar_estoque(session: Session):
    try:
        estoques = session.exec(select(Estoque)).all()
        armazenamentos_dto = [
            ArmazenamentoDTO(
                id=e.id,
                produto=MercadoriaDTO(id=e.produto.id, nome=e.produto.nome, descricao=e.produto.descricao,
                                      status=e.produto.status, data_criacao=e.produto.data_criacao.strftime("%Y-%m-%d"),
                                      preco_base=e.produto.preco_base, categoria=None, marca=None),
                quantidade=e.quantidade,
                data_atualizacao=e.data_atualizacao.strftime("%Y-%m-%d") if e.data_atualizacao else None
            )
            for e in estoques
        ]
        return armazenamentos_dto
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao listar estoques: {e}"
        )
