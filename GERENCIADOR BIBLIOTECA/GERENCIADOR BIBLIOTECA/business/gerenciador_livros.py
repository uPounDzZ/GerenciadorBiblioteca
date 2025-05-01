from models.livro import Livro
from util.memento import Memento

class GerenciadorLivros:
    def __init__(self, livro_dao):
        self._livro_dao = livro_dao
        self._mementos = {}
    
    def cadastrar(self, codigo, titulo, autor, ano, quantidade):
        if self.buscar(codigo):
            raise ValueError(f"Livro com código '{codigo}' já existe")
        
        livro = Livro(codigo, titulo, autor, ano, quantidade)
        return self._livro_dao.salvar(livro)
    
    def buscar(self, codigo):
        return self._livro_dao.buscar(codigo)
    
    def buscar_todos(self):
        return self._livro_dao.buscar_todos()
    
    def atualizar(self, codigo, titulo, autor, ano, quantidade):
        livro = self.buscar(codigo)
        if not livro:
            raise ValueError(f"Livro com código '{codigo}' não encontrado")
        
        self._salvar_memento(livro)
        
        disponivel_ratio = livro.disponivel / livro.quantidade if livro.quantidade > 0 else 1
        novo_disponivel = int(quantidade * disponivel_ratio)
        
        novo_livro = Livro(codigo, titulo, autor, ano, quantidade)
        novo_livro.disponivel = novo_disponivel
        
        return self._livro_dao.atualizar(novo_livro)
    
    def atualizar_disponibilidade(self, livro):
        return self._livro_dao.atualizar(livro)
    
    def deletar(self, codigo):
        livro = self.buscar(codigo)
        if not livro:
            raise ValueError(f"Livro com código '{codigo}' não encontrado")
        
        return self._livro_dao.deletar(codigo)
    
    def _salvar_memento(self, livro):
        novo_livro = Livro(livro.codigo, livro.titulo, livro.autor, livro.ano, livro.quantidade)
        novo_livro.disponivel = livro.disponivel
        self._mementos[livro.codigo] = Memento(novo_livro)
    
    def restaurar_memento(self, codigo=None):
        if codigo is None:
            if not self._mementos:
                raise ValueError("Não há estado anterior para restaurar")
            
            ultimo_codigo = list(self._mementos.keys())[-1]
            return self.restaurar_memento(ultimo_codigo)
        
        if codigo not in self._mementos:
            raise ValueError(f"Não há estado anterior para o livro '{codigo}'")
        
        estado_anterior = self._mementos[codigo].get_estado()
        self._livro_dao.atualizar(estado_anterior)
        del self._mementos[codigo]
        
        return estado_anterior