from ui.menu import Menu
from business.fachada import Fachada
from dao.dao_factory import DAOFactory
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    limpar_tela()
    print("=== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ===")
    print("Como deseja armazenar os dados?")
    print("1. Em memória (RAM)")
    print("2. Em arquivo")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        dao_factory = DAOFactory.get_factory("memoria")
    else:
        dao_factory = DAOFactory.get_factory("arquivo")
    
    fachada = Fachada.get_instance(dao_factory)
    
    if not fachada.buscar_usuario("admin"):
        try:
            fachada.cadastrar_usuario("admin", "Admin123!", True)
            print("Usuário admin criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar usuário admin: {e}")
    
    menu = Menu(fachada)
    menu.exibir()

if __name__ == "__main__":
    main()