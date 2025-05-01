import os
from ui.menu_admin import MenuAdmin
from ui.menu_usuario import MenuUsuario
from util.exceptions import LoginInvalido, SenhaInvalida

class Menu:
    def __init__(self, fachada):
        self._fachada = fachada
        self._usuario_atual = None
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir(self):
        self.limpar_tela()
        print("=== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ===\n")
        
        while True:
            if not self._usuario_atual:
                self._exibir_menu_inicial()
            else:
                if self._usuario_atual.admin:
                    menu_admin = MenuAdmin(self._fachada, self._usuario_atual)
                    self._usuario_atual = menu_admin.exibir()
                else:
                    menu_usuario = MenuUsuario(self._fachada, self._usuario_atual)
                    self._usuario_atual = menu_usuario.exibir()
    
    def _exibir_menu_inicial(self):
        print("\n=== MENU INICIAL ===")
        print("1. Login")
        print("2. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            self._fazer_login()
        elif opcao == "2":
            print("\nObrigado por utilizar o Sistema de Gerenciamento de Biblioteca!")
            exit(0)
        else:
            print("\nOpção inválida. Tente novamente.")
    
    def _fazer_login(self):
        self.limpar_tela()
        print("=== LOGIN ===\n")
        
        login = input("Login: ")
        senha = input("Senha: ")
        
        try:
            usuario = self._fachada.autenticar_usuario(login, senha)
            
            if usuario:
                self._usuario_atual = usuario
                self.limpar_tela()
                print(f"Bem-vindo(a), {login}!")
            else:
                print("\nLogin ou senha incorretos. Tente novamente.")
                input("\nPressione ENTER para continuar...")
        except Exception as e:
            print(f"\nErro ao fazer login: {e}")
            input("\nPressione ENTER para continuar...")