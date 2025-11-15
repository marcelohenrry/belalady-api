from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from dto.cliente_dto import ClienteDTO
from dto.compra_dto import CompraDTO
from dto.pedido_dto import PedidoDTO
from modelo.pedido import Pedido


def salvar_pedido(pedido_dto: PedidoDTO, session: Session):
    try:
        pedido = Pedido(
            data_atualizacao=datetime.now(),
            data_pedido=datetime.strptime(pedido_dto.data_pedido,
                                          "%Y-%m-%d") if pedido_dto.data_pedido else datetime.now(),
            status=pedido_dto.status or "Pendente",
            valor=pedido_dto.valor,
            usuario_id=pedido_dto.usuario_id
        )
        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        return pedido
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao salvar pedido: {e}"
        )


def atualizar_pedido(pedido_id: int, pedido_dto: PedidoDTO, session: Session):
    try:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        pedido.data_atualizacao = datetime.now()
        pedido.status = pedido_dto.status or pedido.status
        pedido.valor = pedido_dto.valor
        pedido.usuario_id = pedido_dto.usuario_id
        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        return pedido
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar pedido: {e}"
        )


def listar_pedidos(session: Session):
    try:
        pedidos = session.exec(select(Pedido)).all()
        compra_dto = [
            CompraDTO(
                id=p.id,
                data_atualizacao=p.data_atualizacao.strftime("%Y-%m-%d") if p.data_atualizacao else None,
                data_pedido=p.data_pedido.strftime("%Y-%m-%d") if p.data_pedido else None,
                status=p.status,
                valor=p.valor,
                usuario=ClienteDTO(id=p.usuario.id, id_provedor=p.usuario.id_provedor, nome=p.usuario.nome,
                                   email=p.usuario.email, fone=p.usuario.fone,
                                   status=p.usuario.status, endereco=None)
            )
            for p in pedidos
        ]
        return compra_dto
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao listar pedidos: {e}"
        )


def buscar_pedido_por_id(pedido_id: int, session: Session):
    try:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        return PedidoDTO(
            id=pedido.id,
            data_atualizacao=pedido.data_atualizacao.strftime("%Y-%m-%d") if pedido.data_atualizacao else None,
            data_pedido=pedido.data_pedido.strftime("%Y-%m-%d") if pedido.data_pedido else None,
            status=pedido.status,
            valor=pedido.valor,
            usuario_id=pedido.usuario_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao buscar pedido: {e}"
        )
