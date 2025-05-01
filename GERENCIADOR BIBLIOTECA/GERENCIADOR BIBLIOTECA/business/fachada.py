from business.gerenciador_usuarios import GerenciadorUsuarios
from business.gerenciador_livros import GerenciadorLivros
from business.gerenciador_emprestimos import GerenciadorEmprestimos
from util.comando import Comando, Invoker

# Singleton e Facade
class Fachada:
    _instance = None
    
    @classmethod
    def get_instance(cls, dao_factory=None):
        if cls._instance is None:
            cls._instance = cls(dao_factory)
        return cls._instance
    
    def __init__(self, dao_factory):
        if self.__class__._instance is not None:
            raise Exception("Esta classe é um Singleton!")
        else:
            self._gerenciador_usuarios = GerenciadorUsuarios(dao_factory.criar_usuario_dao())
            self._gerenciador_livros = GerenciadorLivros(dao_factory.criar_livro_dao())
            self._gerenciador_emprestimos = GerenciadorEmprestimos(dao_factory.criar_emprestimo_dao())
            self._invoker = Invoker()
    
    # Métodos de usuário
    def cadastrar_usuario(self, login, senha, admin=False):
        comando = CadastrarUsuarioComando(self._gerenciador_usuarios, login, senha, admin)
        return self._invoker.executar(comando)
    
    def buscar_usuario(self, login):
        return self._gerenciador_usuarios.buscar(login)
    
    def buscar_todos_usuarios(self):
        return self._gerenciador_usuarios.buscar_todos()
    
    def atualizar_usuario(self, login, senha, admin):
        comando = AtualizarUsuarioComando(self._gerenciador_usuarios, login, senha, admin)
        return self._invoker.executar(comando)
    
    def desfazer_ultima_atualizacao_usuario(self):
        return self._gerenciador_usuarios.restaurar_memento()
    
    def deletar_usuario(self, login):
        comando = DeletarUsuarioComando(self._gerenciador_usuarios, login)
        return self._invoker.executar(comando)
    
    def autenticar_usuario(self, login, senha):
        return self._gerenciador_usuarios.autenticar(login, senha)
    
    # Métodos de livro
    def cadastrar_livro(self, codigo, titulo, autor, ano, quantidade):
        comando = CadastrarLivroComando(self._gerenciador_livros, codigo, titulo, autor, ano, quantidade)
        return self._invoker.executar(comando)
    
    def buscar_livro(self, codigo):
        return self._gerenciador_livros.buscar(codigo)
    
    def buscar_todos_livros(self):
        return self._gerenciador_livros.buscar_todos()
    
    def atualizar_livro(self, codigo, titulo, autor, ano, quantidade):
        comando = AtualizarLivroComando(self._gerenciador_livros, codigo, titulo, autor, ano, quantidade)
        return self._invoker.executar(comando)
    
    def desfazer_ultima_atualizacao_livro(self):
        return self._gerenciador_livros.restaurar_memento()
    
    def deletar_livro(self, codigo):
        comando = DeletarLivroComando(self._gerenciador_livros, codigo)
        return self._invoker.executar(comando)
    
    # Métodos de empréstimo
    def realizar_emprestimo(self, codigo, login_usuario, codigo_livro):
        comando = RealizarEmprestimoComando(self._gerenciador_emprestimos, self._gerenciador_usuarios, 
                                             self._gerenciador_livros, codigo, login_usuario, codigo_livro)
        return self._invoker.executar(comando)
    
    def devolver_livro(self, codigo_emprestimo):
        comando = DevolverLivroComando(self._gerenciador_emprestimos, self._gerenciador_livros, codigo_emprestimo)
        return self._invoker.executar(comando)
    
    def buscar_emprestimo(self, codigo):
        return self._gerenciador_emprestimos.buscar(codigo)
    
    def buscar_todos_emprestimos(self):
        return self._gerenciador_emprestimos.buscar_todos()
    
    def buscar_emprestimos_usuario(self, login_usuario):
        return self._gerenciador_emprestimos.buscar_por_usuario(login_usuario)
    
    # Métodos de relatório
    def gerar_relatorio_acessos(self):
        return self._gerenciador_usuarios.gerar_relatorio_acessos()
    
    def gerar_relatorio_emprestimos(self):
        return self._gerenciador_emprestimos.gerar_relatorio_emprestimos()


# Implementação dos comandos
class CadastrarUsuarioComando(Comando):
    def __init__(self, gerenciador, login, senha, admin):
        self._gerenciador = gerenciador
        self._login = login
        self._senha = senha
        self._admin = admin
    
    def executar(self):
        return self._gerenciador.cadastrar(self._login, self._senha, self._admin)

class AtualizarUsuarioComando(Comando):
    def __init__(self, gerenciador, login, senha, admin):
        self._gerenciador = gerenciador
        self._login = login
        self._senha = senha
        self._admin = admin
    
    def executar(self):
        return self._gerenciador.atualizar(self._login, self._senha, self._admin)

class DeletarUsuarioComando(Comando):
    def __init__(self, gerenciador, login):
        self._gerenciador = gerenciador
        self._login = login
    
    def executar(self):
        return self._gerenciador.deletar(self._login)

class CadastrarLivroComando(Comando):
    def __init__(self, gerenciador, codigo, titulo, autor, ano, quantidade):
        self._gerenciador = gerenciador
        self._codigo = codigo
        self._titulo = titulo
        self._autor = autor
        self._ano = ano
        self._quantidade = quantidade
    
    def executar(self):
        return self._gerenciador.cadastrar(self._codigo, self._titulo, self._autor, self._ano, self._quantidade)

class AtualizarLivroComando(Comando):
    def __init__(self, gerenciador, codigo, titulo, autor, ano, quantidade):
        self._gerenciador = gerenciador
        self._codigo = codigo
        self._titulo = titulo
        self._autor = autor
        self._ano = ano
        self._quantidade = quantidade
    
    def executar(self):
        return self._gerenciador.atualizar(self._codigo, self._titulo, self._autor, self._ano, self._quantidade)

class DeletarLivroComando(Comando):
    def __init__(self, gerenciador, codigo):
        self._gerenciador = gerenciador
        self._codigo = codigo
    
    def executar(self):
        return self._gerenciador.deletar(self._codigo)

class RealizarEmprestimoComando(Comando):
    def __init__(self, gerenciador_emprestimos, gerenciador_usuarios, gerenciador_livros, codigo, login_usuario, codigo_livro):
        self._gerenciador_emprestimos = gerenciador_emprestimos
        self._gerenciador_usuarios = gerenciador_usuarios
        self._gerenciador_livros = gerenciador_livros
        self._codigo = codigo
        self._login_usuario = login_usuario
        self._codigo_livro = codigo_livro
    
    def executar(self):
        usuario = self._gerenciador_usuarios.buscar(self._login_usuario)
        livro = self._gerenciador_livros.buscar(self._codigo_livro)
        
        if not usuario:
            raise ValueError("Usuário não encontrado")
        if not livro:
            raise ValueError("Livro não encontrado")
        if livro.disponivel <= 0:
            raise ValueError("Livro não disponível para empréstimo")
        
        emprestimo = self._gerenciador_emprestimos.realizar(self._codigo, usuario, livro)
        
        # Atualizar disponibilidade do livro
        livro.disponivel -= 1
        self._gerenciador_livros.atualizar_disponibilidade(livro)
        
        return emprestimo

class DevolverLivroComando(Comando):
    def __init__(self, gerenciador_emprestimos, gerenciador_livros, codigo_emprestimo):
        self._gerenciador_emprestimos = gerenciador_emprestimos
        self._gerenciador_livros = gerenciador_livros
        self._codigo_emprestimo = codigo_emprestimo
    
    def executar(self):
        emprestimo = self._gerenciador_emprestimos.buscar(self._codigo_emprestimo)
        
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado")
        if emprestimo.status != "Ativo":
            raise ValueError("Este empréstimo já foi devolvido")
        
        # Atualizar disponibilidade do livro
        livro = emprestimo.livro
        livro.disponivel += 1
        self._gerenciador_livros.atualizar_disponibilidade(livro)
        
        return self._gerenciador_emprestimos.devolver(self._codigo_emprestimo)