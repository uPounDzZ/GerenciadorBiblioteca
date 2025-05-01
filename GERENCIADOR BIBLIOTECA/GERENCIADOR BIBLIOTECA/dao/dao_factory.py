from dao.usuario_dao import UsuarioDAOMemoria, UsuarioDAOArquivo
from dao.livro_dao import LivroDAOMemoria, LivroDAOArquivo
from dao.emprestimo_dao import EmprestimoDAOMemoria, EmprestimoDAOArquivo

class DAOFactory:
    @staticmethod
    def get_factory(tipo):
        if tipo.lower() == "memoria":
            return MemoriaDAOFactory()
        elif tipo.lower() == "arquivo":
            return ArquivoDAOFactory()
        else:
            raise ValueError("Tipo de armazenamento inválido")

class MemoriaDAOFactory:
    def criar_usuario_dao(self):
        return UsuarioDAOMemoria()
    
    def criar_livro_dao(self):
        return LivroDAOMemoria()
    
    def criar_emprestimo_dao(self):
        return EmprestimoDAOMemoria()

class ArquivoDAOFactory:
    def criar_usuario_dao(self):
        return UsuarioDAOArquivo()
    
    def criar_livro_dao(self):
        return LivroDAOArquivo()
    
    def criar_emprestimo_dao(self):
        return EmprestimoDAOArquivo()