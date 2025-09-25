from fastapi import HTTPException
from sqlmodel import Session
from starlette import status

from dto.cliente_dto import ClienteDTO
from modelo.usuario import Usuario, Endereco


def salvar(cliente_dto: ClienteDTO, session: Session):
    try:
        usuario = Usuario(nome=cliente_dto.nome, email=cliente_dto.email, fone=cliente_dto.fone,
                          status=cliente_dto.status)
        session.add(usuario)
        session.flush()
        endereco = Endereco(bairro=cliente_dto.endereco.bairro,
                            cep=cliente_dto.endereco.cep,
                            cidade=cliente_dto.endereco.cidade,
                            complemento=cliente_dto.endereco.complemento,
                            logradouro=cliente_dto.endereco.logradouro,
                            numero=cliente_dto.endereco.numero,
                            usuario_id=usuario.id)

        session.add(endereco)
        session.commit()
        return usuario
    except Exception as e:
        session.rollback()
        print("Erro ao salvar cliente:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao salvar a informação do cliente: {}".format(e)
        )

def atualizar(cliente_dto: ClienteDTO, session: Session):
    try:
        usuario = session.get(Usuario, cliente_dto.id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        usuario.nome = cliente_dto.nome
        usuario.email = cliente_dto.email
        usuario.fone = cliente_dto.fone
        usuario.status = cliente_dto.status

        endereco = session.get(Endereco, cliente_dto.endereco.id)
        if not endereco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endereço não encontrado"
            )

        endereco.bairro = cliente_dto.endereco.bairro
        endereco.cep = cliente_dto.endereco.cep
        endereco.cidade = cliente_dto.endereco.cidade
        endereco.complemento = cliente_dto.endereco.complemento
        endereco.logradouro = cliente_dto.endereco.logradouro
        endereco.numero = cliente_dto.endereco.numero

        session.commit()
        return usuario
    except Exception as e:
        session.rollback()
        print("Erro ao atualizar cliente:", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar a informação do cliente: {}".format(e)
        )