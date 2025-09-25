class Cliente:
    def __init__(self, id, id_provedor, nome, email, fone, status, endereco=None):
        self.id = id
        self.id_provedor = id_provedor
        self.nome = nome
        self.email = email
        self.fone = fone
        self.status = status
        self.endereco = endereco
