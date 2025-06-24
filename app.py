import json
import os
from getpass import getpass
from datetime import datetime

DB_FILE = "db.json"

STATUS_OPTIONS = ["pendente", "em andamento", "concluída"]


def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({"users": [], "tasks": []}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def register():
    db = load_db()
    print("\n=== Cadastro de Usuário ===")
    username = input("Nome de usuário: ").strip()
    if not username:
        print("Nome de usuário não pode ser vazio!")
        return
    if any(u['username'] == username for u in db['users']):
        print("Usuário já existe!")
        return
    password = getpass("Senha: ").strip()
    if not password:
        print("Senha não pode ser vazia!")
        return
    tipo = input("Tipo (usuario/admin): ").strip().lower()
    if tipo not in ["usuario", "admin"]:
        print("Tipo inválido.")
        return
    db['users'].append({"username": username, "password": password, "tipo": tipo})
    save_db(db)
    print("Usuário cadastrado com sucesso!")

def login():
    db = load_db()
    print("\n=== Login ===")
    username = input("Usuário: ").strip()
    password = getpass("Senha: ").strip()
    user = next((u for u in db['users'] if u['username'] == username and u['password'] == password), None)
    if user:
        print(f"Bem-vindo, {user['username']}!\n")
        return user
    print("Usuário ou senha incorretos.")
    return None

def criar_tarefa(user):
    db = load_db()
    print("\n=== Criar Nova Tarefa ===")
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    status = input("Status (pendente/em andamento/concluída): ").strip().lower()
    if not titulo or not descricao:
        print("Título e descrição são obrigatórios.")
        return
    if status not in STATUS_OPTIONS:
        status = "pendente"
    novo_id = max([t['id'] for t in db['tasks']], default=0) + 1
    tarefa = {
        "id": novo_id,
        "titulo": titulo,
        "descricao": descricao,
        "status": status,
        "criado_por": user['username'],
        "data": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    db['tasks'].append(tarefa)
    save_db(db)
    print("Tarefa criada com sucesso!")

def listar_tarefas(user):
    db = load_db()
    print("\n=== Lista de Tarefas ===")
    encontrou = False
    for t in db['tasks']:
        if user['tipo'] == 'admin' or t['criado_por'] == user['username']:
            encontrou = True
            print(f"[{t['id']}] {t['titulo']} ({t['criado_por']}) - {t['data']} - Status: {t.get('status', 'pendente')}")
            print(f"    {t['descricao']}\n")
    if not encontrou:
        print("Nenhuma tarefa encontrada.")

def editar_tarefa(user):
    db = load_db()
    listar_tarefas(user)
    tarefa_id = input("ID da tarefa para editar: ").strip()
    for t in db['tasks']:
        if str(t['id']) == tarefa_id and (user['tipo'] == 'admin' or t['criado_por'] == user['username']):
            novo_titulo = input(f"Novo título (atual: {t['titulo']}): ").strip()
            nova_desc = input(f"Nova descrição (atual: {t['descricao']}): ").strip()
            novo_status = input(f"Novo status (atual: {t.get('status', 'pendente')}): ").strip().lower()
            if novo_titulo:
                t['titulo'] = novo_titulo
            if nova_desc:
                t['descricao'] = nova_desc
            if novo_status in STATUS_OPTIONS:
                t['status'] = novo_status
            save_db(db)
            print("Tarefa atualizada.")
            return
    print("Tarefa não encontrada ou sem permissão.")

def excluir_tarefa(user):
    db = load_db()
    listar_tarefas(user)
    tarefa_id = input("ID da tarefa para excluir: ").strip()
    for t in db['tasks']:
        if str(t['id']) == tarefa_id and (user['tipo'] == 'admin' or t['criado_por'] == user['username']):
            db['tasks'].remove(t)
            save_db(db)
            print("Tarefa excluída.")
            return
    print("Tarefa não encontrada ou sem permissão.")

def menu_usuario(user):
    while True:
        print("\n=== MENU USUÁRIO ===")
        print("1 - Criar tarefa")
        print("2 - Ver tarefas")
        print("3 - Editar tarefa")
        print("4 - Excluir tarefa")
        print("5 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == '1':
            criar_tarefa(user)
        elif opcao == '2':
            listar_tarefas(user)
        elif opcao == '3':
            editar_tarefa(user)
        elif opcao == '4':
            excluir_tarefa(user)
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

def menu_admin(user):
    while True:
        print("\n=== MENU ADMIN ===")
        print("1 - Criar tarefa")
        print("2 - Ver todas as tarefas")
        print("3 - Editar tarefa")
        print("4 - Excluir tarefa")
        print("5 - Criar novo usuário")
        print("6 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == '1':
            criar_tarefa(user)
        elif opcao == '2':
            listar_tarefas(user)
        elif opcao == '3':
            editar_tarefa(user)
        elif opcao == '4':
            excluir_tarefa(user)
        elif opcao == '5':
            register()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

def main():
    clear()
    print("=== Sistema GRUD de Tarefas ===")
    while True:
        print("\n1 - Login")
        print("2 - Cadastrar")
        print("3 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == '1':
            user = login()
            if user:
                clear()
                if user['tipo'] == 'admin':
                    menu_admin(user)
                else:
                    menu_usuario(user)
                clear()
        elif opcao == '2':
            register()
        elif opcao == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    main()
