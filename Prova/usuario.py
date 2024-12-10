import json
from pesquisa import Pesquisa

class Usuario():
    def __init__(self, nome, senha, historico):
        self.nome = nome
        self.senha = senha
        self.historico = historico if historico != None else []

    def add_historico(self, pesquisa):
        self.historico.append(pesquisa)
        editar_historico(self)

def editar_historico(usuario):
    try:
        with open('usuarios.json', 'r') as file:
            usuarios = json.load(file)
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")
        return False

    for i, user in enumerate(usuarios):
        if user['nome'] == usuario.nome:
            usuarios[i]['historico'] = []
            for pesquisa in usuario.historico:
                cidade = pesquisa.cidade
                start_date = pesquisa.start_date
                end_date = pesquisa.end_date
                usuarios[i]['historico'].append({'cidade': cidade, 'start_date': start_date, 'end_date': end_date})
            break
    
    with open('usuarios.json', 'w') as file:
        json.dump(usuarios, file, indent=4)
    


def registrar_usuario(usuario):
    try:
        with open('usuarios.json', 'r') as file:
            usuarios = json.load(file)
    except FileNotFoundError:
        usuarios = []

    for u in usuarios:
        if u['nome'] == usuario.nome:
            print("Usuário já existe.")
            return False

    usuarios.append({"nome": usuario.nome, "senha": usuario.senha, "historico": []})

    with open("usuarios.json", "w") as file:
        json.dump(usuarios, file, indent=4)
    return True

def carregar_usuarios():
    try:
        with open("usuarios.json", "r") as file:
            data = json.load(file)
            lista = []
            for u in data:
                historico = []
                for i in u["historico"]:
                    p = Pesquisa(i["cidade"], i["start_date"], i["end_date"])
                    historico.append(p)
                lista.append(Usuario(u["nome"], u["senha"], historico))
            return lista
    except FileNotFoundError:
        return []