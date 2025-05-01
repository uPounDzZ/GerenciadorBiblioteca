import os
import random
from util.exceptions import LoginInvalido, SenhaInvalida

class MenuAdmin:
    def __init__(self, fachada, usuario):
        self._fachada = fachada
        self._usuario = usuario
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir(self):
        while True:
            self.limpar_tela()
            print(f"=== MENU ADMINISTRADOR - {self._usuario.login} ===\n")
            print("== Usuários ==")
            print("1. Cadastrar usuário")
            print("2. Listar usuários")
            print("3. Editar usuário")
            print("4. Desfazer última atualização de usuário")
            print("5. Excluir usuário")
            
            print("\n== Livros ==")
            print("6. Cadastrar livro")
            print("7. Listar livros")
            print("8. Editar livro")
            print("9. Desfazer última atualização de livro")
            print("10. Excluir livro")
            
            print("\n== Empréstimos ==")
            print("11. Realizar empréstimo")
            print("12. Devolver livro")
            print("13. Listar empréstimos")
            
            print("\n== Relatórios ==")
            print("14. Relatório de acessos")
            print("15. Relatório de empréstimos")
            
            print("\n0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "0":
                return None
            elif opcao == "1":
                self._cadastrar_usuario()
            elif opcao == "2":
                self._listar_usuarios()
            elif opcao == "3":
                self._editar_usuario()
            elif opcao == "4":
                self._desfazer_atualizacao_usuario()
            elif opcao == "5":
                self._excluir_usuario()
            elif opcao == "6":
                self._cadastrar_livro()
            elif opcao == "7":
                self._listar_livros()
            elif opcao == "8":
                self._editar_livro()
            elif opcao == "9":
                self._desfazer_atualizacao_livro()
            elif opcao == "10":
                self._excluir_livro()
            elif opcao == "11":
                self._realizar_emprestimo()
            elif opcao == "12":
                self._devolver_livro()
            elif opcao == "13":
                self._listar_emprestimos()
            elif opcao == "14":
                self._gerar_relatorio_acessos()
            elif opcao == "15":
                self._gerar_relatorio_emprestimos()
            else:
                print("\nOpção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar...")
        
        return self._usuario
    
    def _cadastrar_usuario(self):
        self.limpar_tela()
        print("=== CADASTRAR USUÁRIO ===\n")
        
        login = input("Login (máx. 12 caracteres, sem números): ")
        senha = input("Senha (mín. 8 caracteres, com maiúscula, minúscula, número e caractere especial): ")
        
        admin_opcao = input("Perfil de administrador (S/N)? ").upper()
        admin = admin_opcao == "S"
        
        try:
            self._fachada.cadastrar_usuario(login, senha, admin)
            print("\nUsuário cadastrado com sucesso!")
        except (LoginInvalido, SenhaInvalida, ValueError) as e:
            print(f"\nErro ao cadastrar usuário: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _listar_usuarios(self):
        self.limpar_tela()
        print("=== LISTA DE USUÁRIOS ===\n")
        
        usuarios = self._fachada.buscar_todos_usuarios()
        
        if not usuarios:
            print("Nenhum usuário cadastrado.")
        else:
            for i, usuario in enumerate(usuarios, 1):
                print(f"{i}. {usuario}")
        
        input("\nPressione ENTER para continuar...")
    
    def _editar_usuario(self):
        self.limpar_tela()
        print("=== EDITAR USUÁRIO ===\n")
        
        login = input("Login do usuário a editar: ")
        
        usuario = self._fachada.buscar_usuario(login)
        if not usuario:
            print(f"\nUsuário '{login}' não encontrado.")
            input("\nPressione ENTER para continuar...")
            return
        
        print(f"\nEditando usuário: {usuario}")
        
        senha = input("Nova senha (deixe em branco para manter): ")
        if not senha:
            senha = usuario.senha
        
        admin_opcao = input(f"Perfil de administrador (S/N) [{'S' if usuario.admin else 'N'}]? ").upper()
        admin = admin_opcao == "S" if admin_opcao else usuario.admin
        
        try:
            self._fachada.atualizar_usuario(login, senha, admin)
            print("\nUsuário atualizado com sucesso!")
        except (LoginInvalido, SenhaInvalida, ValueError) as e:
            print(f"\nErro ao atualizar usuário: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _desfazer_atualizacao_usuario(self):
        self.limpar_tela()
        print("=== DESFAZER ÚLTIMA ATUALIZAÇÃO DE USUÁRIO ===\n")
        
        try:
            usuario = self._fachada.desfazer_ultima_atualizacao_usuario()
            print(f"\nAtualização desfeita. Estado restaurado: {usuario}")
        except ValueError as e:
            print(f"\nErro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _excluir_usuario(self):
        self.limpar_tela()
        print("=== EXCLUIR USUÁRIO ===\n")
        
        login = input("Login do usuário a excluir: ")
        
        if login == self._usuario.login:
            print("\nVocê não pode excluir seu próprio usuário!")
            input("\nPressione ENTER para continuar...")
            return
        
        if login == "admin":
            print("\nNão é possível excluir o usuário administrador padrão.")
            input("\nPressione ENTER para continuar...")
            return
        
        usuario = self._fachada.buscar_usuario(login)
        if not usuario:
            print(f"\nUsuário '{login}' não encontrado.")
            input("\nPressione ENTER para continuar...")
            return
        
        confirmacao = input(f"Confirma exclusão do usuário '{login}' (S/N)? ").upper()
        if confirmacao == "S":
            try:
                self._fachada.deletar_usuario(login)
                print("\nUsuário excluído com sucesso!")
            except ValueError as e:
                print(f"\nErro ao excluir usuário: {e}")
        else:
            print("\nOperação cancelada.")
        
        input("\nPressione ENTER para continuar...")
    
    def _cadastrar_livro(self):
        self.limpar_tela()
        print("=== CADASTRAR LIVRO ===\n")
        
        codigo = input("Código: ")
        titulo = input("Título: ")
        autor = input("Autor: ")
        
        try:
            ano = int(input("Ano de publicação: "))
            quantidade = int(input("Quantidade: "))
            
            self._fachada.cadastrar_livro(codigo, titulo, autor, ano, quantidade)
            print("\nLivro cadastrado com sucesso!")
        except ValueError as e:
            print(f"\nErro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _listar_livros(self):
        self.limpar_tela()
        print("=== LISTA DE LIVROS ===\n")
        
        livros = self._fachada.buscar_todos_livros()
        
        if not livros:
            print("Nenhum livro cadastrado.")
        else:
            for i, livro in enumerate(livros, 1):
                print(f"{i}. {livro}")
        
        input("\nPressione ENTER para continuar...")
    
    def _editar_livro(self):
        self.limpar_tela()
        print("=== EDITAR LIVRO ===\n")
        
        codigo = input("Código do livro a editar: ")
        
        livro = self._fachada.buscar_livro(codigo)
        if not livro:
            print(f"\nLivro com código '{codigo}' não encontrado.")
            input("\nPressione ENTER para continuar...")
            return
        
        print(f"\nEditando livro: {livro}")
        
        titulo = input(f"Título [{livro.titulo}]: ") or livro.titulo
        autor = input(f"Autor [{livro.autor}]: ") or livro.autor
        
        try:
            ano_input = input(f"Ano de publicação [{livro.ano}]: ")
            ano = int(ano_input) if ano_input else livro.ano
            
            qtd_input = input(f"Quantidade [{livro.quantidade}]: ")
            quantidade = int(qtd_input) if qtd_input else livro.quantidade
            
            self._fachada.atualizar_livro(codigo, titulo, autor, ano, quantidade)
            print("\nLivro atualizado com sucesso!")
        except ValueError as e:
            print(f"\nErro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _desfazer_atualizacao_livro(self):
        self.limpar_tela()
        print("=== DESFAZER ÚLTIMA ATUALIZAÇÃO DE LIVRO ===\n")
        
        try:
            livro = self._fachada.desfazer_ultima_atualizacao_livro()
            print(f"\nAtualização desfeita. Estado restaurado: {livro}")
        except ValueError as e:
            print(f"\nErro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _excluir_livro(self):
        self.limpar_tela()
        print("=== EXCLUIR LIVRO ===\n")
        
        codigo = input("Código do livro a excluir: ")
        
        livro = self._fachada.buscar_livro(codigo)
        if not livro:
            print(f"\nLivro com código '{codigo}' não encontrado.")
            input("\nPressione ENTER para continuar...")
            return
        
        confirmacao = input(f"Confirma exclusão do livro '{livro.titulo}' (S/N)? ").upper()
        if confirmacao == "S":
            try:
                self._fachada.deletar_livro(codigo)
                print("\nLivro excluído com sucesso!")
            except ValueError as e:
                print(f"\nErro ao excluir livro: {e}")
        else:
            print("\nOperação cancelada.")
        
        input("\nPressione ENTER para continuar...")
    
    def _realizar_emprestimo(self):
        self.limpar_tela()
        print("=== REALIZAR EMPRÉSTIMO ===\n")
        
        codigo = codigo = f"EMP{random.randint(0000, 9999)}"
        login_usuario = input("Login do usuário: ")
        codigo_livro = input("Código do livro: ")
        
        try:
            emprestimo = self._fachada.realizar_emprestimo(codigo, login_usuario, codigo_livro)
            print("\nEmpréstimo realizado com sucesso!")
            print(f"Detalhes: {emprestimo}")
        except ValueError as e:
            print(f"\nErro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _devolver_livro(self):
        self.limpar_tela()
        print("=== DEVOLVER LIVRO ===\n")
        
        codigo_emprestimo = input("Código do empréstimo: ")
        
        try:
            emprestimo = self._fachada.devolver_livro(codigo_emprestimo)
            print("\nLivro devolvido com sucesso!")
            print(f"Detalhes: {emprestimo}")
        except ValueError as e:
            print(f"\nErro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _listar_emprestimos(self):
        self.limpar_tela()
        print("=== LISTA DE EMPRÉSTIMOS ===\n")
        
        emprestimos = self._fachada.buscar_todos_emprestimos()
        
        if not emprestimos:
            print("Nenhum empréstimo registrado.")
        else:
            for i, emprestimo in enumerate(emprestimos, 1):
                print(f"{i}. {emprestimo}")
        
        input("\nPressione ENTER para continuar...")
    
    def _gerar_relatorio_acessos(self):
        self.limpar_tela()
        print("=== RELATÓRIO DE ACESSOS DOS USUÁRIOS ===\n")
        
        relatorio = self._fachada.gerar_relatorio_acessos()
        print(relatorio)
        
        input("\nPressione ENTER para continuar...")
    
    def _gerar_relatorio_emprestimos(self):
        self.limpar_tela()
        print("=== RELATÓRIO DE EMPRÉSTIMOS ===\n")
        
        relatorio = self._fachada.gerar_relatorio_emprestimos()
        print(relatorio)
        
        input("\nPressione ENTER para continuar...")