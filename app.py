import getpass
import json
from colorama import Fore, Style, init

init(autoreset=True)

class Student:
    def __init__(self, nome, disciplina, matricula, senha):
        self.nome = nome
        self.disciplina = disciplina
        self.matricula = matricula
        self.senha = senha

    def __str__(self):
        return f"{Fore.CYAN}Nome: {self.nome}\nDisciplina: {self.disciplina}\nMatrícula: {self.matricula}" + Style.RESET_ALL

    def to_dict(self):
        return {
            "nome": self.nome,
            "disciplina": self.disciplina,
            "matricula": self.matricula,
            "senha": self.senha,
        }

    @staticmethod
    def from_dict(data):
        return Student(data["nome"], data["disciplina"], data["matricula"], data["senha"])


class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def hash(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, password, index):
        h = self.hash(password)
        self.table[h] = index

    def get(self, password):
        h = self.hash(password)
        return self.table[h]


class StudentManager:
    def __init__(self, filename="students.json"):
        self.students = []
        self.hash_table = HashTable()
        self.filename = filename
        self.load_students()

    def save_students(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, ensure_ascii=False, indent=4)

    def load_students(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
                self.students.sort(key=lambda a: a.matricula)
                self.rebuild_hash_table()
        except FileNotFoundError:
            pass  # arquivo não existe ainda

    def add_student(self):
        if len(self.students) < 20:
            nome = input("Nome: ").strip()
            disciplina = input("Disciplina: ").strip()
            matricula = input("Número de Matrícula: ").strip()
            if any(aluno.matricula == matricula for aluno in self.students):
                print(Fore.YELLOW + "Matrícula já cadastrada.")
                return
            senha = getpass.getpass("Senha: ").strip()
            aluno = Student(nome, disciplina, matricula, senha)
            self.students.append(aluno)
            self.students.sort(key=lambda a: a.matricula)
            self.rebuild_hash_table()
            self.save_students()
            print(Fore.GREEN + "Aluno cadastrado com sucesso!")
        else:
            print(Fore.RED + "Limite de alunos atingido.")

    def rebuild_hash_table(self):
        self.hash_table = HashTable()
        for i, aluno in enumerate(self.students):
            self.hash_table.insert(aluno.senha, i)

    def find_student_by_password(self, senha):
        index = self.hash_table.get(senha)
        if index is not None and index < len(self.students):
            return self.students[index]
        return None

    def binary_search(self, matricula):
        inicio, fim = 0, len(self.students) - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            if self.students[meio].matricula == matricula:
                return meio
            elif self.students[meio].matricula < matricula:
                inicio = meio + 1
            else:
                fim = meio - 1
        return -1

    def display_student(self, senha):
        aluno = self.find_student_by_password(senha)
        if aluno:
            print(Fore.MAGENTA + "\n=== Dados do Aluno ===")
            print(aluno)
        else:
            print(Fore.RED + "Aluno não encontrado ou senha incorreta.")

    def display_student_admin(self, matricula):
        index = self.binary_search(matricula)
        if index != -1:
            print(Fore.BLUE + "\n=== Dados do Aluno ===")
            print(self.students[index])
        else:
            print(Fore.RED + "Aluno não encontrado.")

    def listar_alunos(self):
        if not self.students:
            print(Fore.YELLOW + "Nenhum aluno cadastrado.")
            return
        print(Fore.CYAN + "\n=== Lista de Alunos ===")
        for aluno in self.students:
            print(aluno)
            print(Fore.LIGHTBLACK_EX + "-" * 30)

    def remover_aluno(self):
        matricula = input("Digite a matrícula do aluno a ser removido: ").strip()
        index = self.binary_search(matricula)
        if index != -1:
            del self.students[index]
            self.rebuild_hash_table()
            self.save_students()
            print(Fore.GREEN + "Aluno removido com sucesso.")
        else:
            print(Fore.RED + "Aluno não encontrado.")

    def alterar_disciplina(self):
        matricula = input("Digite a matrícula do aluno: ").strip()
        index = self.binary_search(matricula)
        if index != -1:
            nova_disciplina = input("Nova disciplina: ").strip()
            self.students[index].disciplina = nova_disciplina
            self.save_students()
            print(Fore.GREEN + "Disciplina atualizada com sucesso!")
        else:
            print(Fore.RED + "Aluno não encontrado.")


def menu():
    manager = StudentManager()
    while True:
        print(Fore.YELLOW + "\n=== Sistema de Gerenciamento de Alunos ===")
        print("1 - Acesso como Aluno")
        print("2 - Acesso como Administrador")
        print("3 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == '1':
            senha = getpass.getpass("Digite sua senha: ").strip()
            manager.display_student(senha)

        elif opcao == '2':
            while True:
                print(Fore.YELLOW + "\n--- Menu do Administrador ---")
                print("1 - Cadastrar Aluno")
                print("2 - Buscar por Matrícula")
                print("3 - Listar Todos os Alunos")
                print("4 - Remover Aluno")
                print("5 - Alterar Disciplina do Aluno")
                print("6 - Voltar ao Menu Principal")
                admin_opcao = input("Escolha: ").strip()
                if admin_opcao == '1':
                    manager.add_student()
                elif admin_opcao == '2':
                    matricula = input("Digite a matrícula: ").strip()
                    manager.display_student_admin(matricula)
                elif admin_opcao == '3':
                    manager.listar_alunos()
                elif admin_opcao == '4':
                    manager.remover_aluno()
                elif admin_opcao == '5':
                    manager.alterar_disciplina()
                elif admin_opcao == '6':
                    break
                else:
                    print(Fore.RED + "Opção inválida.")

        elif opcao == '3':
            print(Fore.LIGHTBLUE_EX + "Saindo...")
            break
        else:
            print(Fore.RED + "Opção inválida.")


if __name__ == "__main__":
    menu()
