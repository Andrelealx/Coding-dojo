import getpass

class Student:
    def __init__(self, nome, disciplina, matricula, senha):
        self.nome = nome
        self.disciplina = disciplina
        self.matricula = matricula
        self.senha = senha

    def __str__(self):
        return f"Nome: {self.nome}\nDisciplina: {self.disciplina}\nMatrícula: {self.matricula}"


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
    def __init__(self):
        self.students = []
        self.hash_table = HashTable()

    def add_student(self):
        if len(self.students) < 20:
            nome = input("Nome: ").strip()
            disciplina = input("Disciplina: ").strip()
            matricula = input("Número de Matrícula: ").strip()
            if any(aluno.matricula == matricula for aluno in self.students):
                print("Matrícula já cadastrada.")
                return
            senha = getpass.getpass("Senha: ").strip()
            aluno = Student(nome, disciplina, matricula, senha)
            self.students.append(aluno)
            self.students.sort(key=lambda a: a.matricula)
            self.rebuild_hash_table()
            print("Aluno cadastrado com sucesso!")
        else:
            print("Limite de alunos atingido.")

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
            print("\n=== Dados do Aluno ===")
            print(aluno)
        else:
            print("Aluno não encontrado ou senha incorreta.")

    def display_student_admin(self, matricula):
        index = self.binary_search(matricula)
        if index != -1:
            print("\n=== Dados do Aluno ===")
            print(self.students[index])
        else:
            print("Aluno não encontrado.")

    def listar_alunos(self):
        if not self.students:
            print("Nenhum aluno cadastrado.")
            return
        print("\n=== Lista de Alunos ===")
        for aluno in self.students:
            print(aluno)
            print("-" * 30)

    def remover_aluno(self):
        matricula = input("Digite a matrícula do aluno a ser removido: ").strip()
        index = self.binary_search(matricula)
        if index != -1:
            del self.students[index]
            self.rebuild_hash_table()
            print("Aluno removido com sucesso.")
        else:
            print("Aluno não encontrado.")


def menu():
    manager = StudentManager()
    while True:
        print("\n=== Sistema de Gerenciamento de Alunos ===")
        print("1 - Acesso como Aluno")
        print("2 - Acesso como Administrador")
        print("3 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == '1':
            senha = getpass.getpass("Digite sua senha: ").strip()
            manager.display_student(senha)

        elif opcao == '2':
            while True:
                print("\n--- Menu do Administrador ---")
                print("1 - Cadastrar Aluno")
                print("2 - Buscar por Matrícula")
                print("3 - Listar Todos os Alunos")
                print("4 - Remover Aluno")
                print("5 - Voltar ao Menu Principal")
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
                    break
                else:
                    print("Opção inválida.")

        elif opcao == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
