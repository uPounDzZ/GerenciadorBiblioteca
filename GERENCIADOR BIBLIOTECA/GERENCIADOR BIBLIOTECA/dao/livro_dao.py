import pickle
import os
from dao.abstract_dao import AbstractDAO

class LivroDAOMemoria(AbstractDAO):
    def __init__(self):
        self._livros = {}
    
    def salvar(self, livro):
        self._livros[livro.codigo] = livro
        return livro
    
    def buscar(self, codigo):
        return self._livros.get(codigo)
    
    def buscar_todos(self):
        return list(self._livros.values())
    
    def atualizar(self, livro):
        if livro.codigo in self._livros:
            self._livros[livro.codigo] = livro
            return livro
        return None
    
    def deletar(self, codigo):
        if codigo in self._livros:
            del self._livros[codigo]
            return True
        return False

class LivroDAOArquivo(AbstractDAO):
    def __init__(self):
        self._arquivo = "livros.dat"
        if not os.path.exists(self._arquivo):
            with open(self._arquivo, 'wb') as f:
                pickle.dump({}, f)
    
    def _carregar(self):
        try:
            with open(self._arquivo, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    
    def _salvar_todos(self, livros):
        with open(self._arquivo, 'wb') as f:
            pickle.dump(livros, f)
    
    def salvar(self, livro):
        livros = self._carregar()
        livros[livro.codigo] = livro
        self._salvar_todos(livros)
        return livro
    
    def buscar(self, codigo):
        livros = self._carregar()
        return livros.get(codigo)
    
    def buscar_todos(self):
        livros = self._carregar()
        return list(livros.values())
    
    def atualizar(self, livro):
        livros = self._carregar()
        if livro.codigo in livros:
            livros[livro.codigo] = livro
            self._salvar_todos(livros)
            return livro
        return None
    
    def deletar(self, codigo):
        livros = self._carregar()
        if codigo in livros:
            del livros[codigo]
            self._salvar_todos(livros)
            return True
        return False