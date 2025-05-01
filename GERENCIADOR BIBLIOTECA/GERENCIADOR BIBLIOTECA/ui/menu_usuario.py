import os

class MenuUsuario:
    def __init__(self, fachada, usuario):
        self._fachada = fachada
        self._usuario = usuario
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir(self):
        while True:
            self.limpar_tela()
            print(f"=== MENU USUÁRIO - {self._usuario.login} ===\n")
            print("1. Consultar livros disponíveis")
            print("2. Meus empréstimos")
            print("3. Buscar livro por título")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "0":
                return None
            elif opcao == "1":
                self._listar_livros_disponiveis()
            elif opcao == "2":
                self._listar_meus_emprestimos()
            elif opcao == "3":
                self._buscar_livro_por_titulo()
            else:
                print("\nOpção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar...")
        
        return self._usuario
    
    def _listar_livros_disponiveis(self):
        self.limpar_tela()
        print("=== LIVROS DISPONÍVEIS ===\n")
        
        livros = self._fachada.buscar_todos_livros()
        livros_disponiveis = [livro for livro in livros if livro.disponivel > 0]
        
        if not livros_disponiveis:
            print("Nenhum livro disponível no momento.")
        else:
            for i, livro in enumerate(livros_disponiveis, 1):
                print(f"{i}. {livro}")
        
        input("\nPressione ENTER para continuar...")
    
    def _listar_meus_emprestimos(self):
        self.limpar_tela()
        print("=== MEUS EMPRÉSTIMOS ===\n")
        
        emprestimos = self._fachada.buscar_emprestimos_usuario(self._usuario.login)
        
        if not emprestimos:
            print("Você não possui empréstimos registrados.")
        else:
            for i, emprestimo in enumerate(emprestimos, 1):
                print(f"{i}. {emprestimo}")
        
        input("\nPressione ENTER para continuar...")
    
    def _buscar_livro_por_titulo(self):
        self.limpar_tela()
        print("=== BUSCAR LIVRO POR TÍTULO ===\n")
        
        titulo = input("Digite parte do título: ").lower()
        
        livros = self._fachada.buscar_todos_livros()
        livros_encontrados = [livro for livro in livros if titulo in livro.titulo.lower()]
        
        print(f"\nResultados da busca por '{titulo}':")
        
        if not livros_encontrados:
            print("Nenhum livro encontrado.")
        else:
            for i, livro in enumerate(livros_encontrados, 1):
                print(f"{i}. {livro}")
        
        input("\nPressione ENTER para continuar...")