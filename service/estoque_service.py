from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from dto.estoque_dto import EstoqueDTO, EstoqueCreateDTO, EstoqueUpdateDTO, AjusteEstoqueDTO
from modelo.estoque import Estoque


def salvar_estoque(estoque_dto: EstoqueCreateDTO, session: Session):
    try:
        print("Salvando estoque:", estoque_dto)

        # Verifica se já existe estoque para este produto
        statement = select(Estoque).where(Estoque.produto_id == estoque_dto.produto_id)
        estoque_existente = session.exec(statement).first()

        if estoque_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe estoque cadastrado para o produto ID {estoque_dto.produto_id}"
            )

        estoque = Estoque(
            produto_id=estoque_dto.produto_id,
            quantidade=estoque_dto.quantidade,
            data_atualizacao=datetime.now()
        )
        session.add(estoque)
        session.commit()
        session.refresh(estoque)
        return estoque
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print("Erro ao salvar estoque:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao salvar a informação do estoque: {}".format(e)
        )


def atualizar(estoque_id: int, estoque_dto: EstoqueUpdateDTO, session: Session):
    try:
        estoque = session.get(Estoque, estoque_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado"
            )

        if estoque_dto.quantidade is not None:
            estoque.quantidade = estoque_dto.quantidade
            estoque.data_atualizacao = datetime.now()

        session.add(estoque)
        session.commit()
        session.refresh(estoque)
        return estoque
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar estoque:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar a informação do estoque: {}".format(e)
        )


def ajustar_estoque(produto_id: int, ajuste_dto: AjusteEstoqueDTO, session: Session):
    try:
        # Busca o estoque pelo produto_id
        statement = select(Estoque).where(Estoque.produto_id == produto_id)
        estoque = session.exec(statement).first()

        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estoque não encontrado para o produto ID {produto_id}"
            )

        # Ajusta a quantidade baseado no tipo
        if ajuste_dto.tipo_ajuste.lower() == "entrada":
            estoque.quantidade += ajuste_dto.quantidade
        elif ajuste_dto.tipo_ajuste.lower() == "saida":
            if estoque.quantidade < ajuste_dto.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Quantidade insuficiente. Disponível: {estoque.quantidade}"
                )
            estoque.quantidade -= ajuste_dto.quantidade
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de ajuste inválido. Use 'entrada' ou 'saida'"
            )

        estoque.data_atualizacao = datetime.now()

        session.add(estoque)
        session.commit()
        session.refresh(estoque)

        print(f"Ajuste de estoque realizado: {ajuste_dto.tipo_ajuste} de {ajuste_dto.quantidade} unidades")
        return estoque
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print("Erro ao ajustar estoque:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao ajustar estoque: {}".format(e)
        )


def listar(session: Session):
    try:
        estoques = session.exec(select(Estoque)).all()
        print("Estoques encontrados:", estoques)
        estoques_dto = [
            EstoqueDTO(
                id=e.id,
                produto_id=e.produto_id,
                quantidade=e.quantidade,
                data_atualizacao=e.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S") if e.data_atualizacao else None
            )
            for e in estoques
        ]
        return estoques_dto
    except Exception as e:
        print("Erro ao listar estoques:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao listar estoques: {}".format(e)
        )


def buscar_por_id(estoque_id: int, session: Session):
    try:
        estoque = session.get(Estoque, estoque_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado"
            )
        estoque_dto = EstoqueDTO(
            id=estoque.id,
            produto_id=estoque.produto_id,
            quantidade=estoque.quantidade,
            data_atualizacao=estoque.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S") if estoque.data_atualizacao else None
        )
        return estoque_dto
    except HTTPException:
        raise
    except Exception as e:
        print("Erro ao buscar estoque:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao buscar estoque: {}".format(e)
        )


def buscar_por_produto(produto_id: int, session: Session):
    try:
        statement = select(Estoque).where(Estoque.produto_id == produto_id)
        estoque = session.exec(statement).first()

        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estoque não encontrado para o produto ID {produto_id}"
            )

        estoque_dto = EstoqueDTO(
            id=estoque.id,
            produto_id=estoque.produto_id,
            quantidade=estoque.quantidade,
            data_atualizacao=estoque.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S") if estoque.data_atualizacao else None
        )
        return estoque_dto
    except HTTPException:
        raise
    except Exception as e:
        print("Erro ao buscar estoque por produto:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao buscar estoque: {}".format(e)
        )


def deletar(estoque_id: int, session: Session):
    try:
        estoque = session.get(Estoque, estoque_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado"
            )
        session.delete(estoque)
        session.commit()
        return {"detail": "Estoque deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print("Erro ao deletar estoque:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao deletar estoque: {}".format(e)
        )