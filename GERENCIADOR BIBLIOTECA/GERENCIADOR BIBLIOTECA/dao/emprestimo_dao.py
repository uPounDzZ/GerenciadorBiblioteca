import pickle
import os
from dao.abstract_dao import AbstractDAO

class EmprestimoDAOMemoria(AbstractDAO):
    def __init__(self):
        self._emprestimos = {}
    
    def salvar(self, emprestimo):
        self._emprestimos[emprestimo.codigo] = emprestimo
        return emprestimo
    
    def buscar(self, codigo):
        return self._emprestimos.get(codigo)
    
    def buscar_todos(self):
        return list(self._emprestimos.values())
    
    def atualizar(self, emprestimo):
        if emprestimo.codigo in self._emprestimos:
            self._emprestimos[emprestimo.codigo] = emprestimo
            return emprestimo
        return None
    
    def deletar(self, codigo):
        if codigo in self._emprestimos:
            del self._emprestimos[codigo]
            return True
        return False

class EmprestimoDAOArquivo(AbstractDAO):
    def __init__(self):
        self._arquivo = "emprestimos.dat"
        if not os.path.exists(self._arquivo):
            with open(self._arquivo, 'wb') as f:
                pickle.dump({}, f)
    
    def _carregar(self):
        try:
            with open(self._arquivo, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    
    def _salvar_todos(self, emprestimos):
        with open(self._arquivo, 'wb') as f:
            pickle.dump(emprestimos, f)
    
    def salvar(self, emprestimo):
        emprestimos = self._carregar()
        emprestimos[emprestimo.codigo] = emprestimo
        self._salvar_todos(emprestimos)
        return emprestimo
    
    def buscar(self, codigo):
        emprestimos = self._carregar()
        return emprestimos.get(codigo)
    
    def buscar_todos(self):
        emprestimos = self._carregar()
        return list(emprestimos.values())
    
    def atualizar(self, emprestimo):
        emprestimos = self._carregar()
        if emprestimo.codigo in emprestimos:
            emprestimos[emprestimo.codigo] = emprestimo
            self._salvar_todos(emprestimos)
            return emprestimo
        return None
    
    def deletar(self, codigo):
        emprestimos = self._carregar()
        if codigo in emprestimos:
            del emprestimos[codigo]
            self._salvar_todos(emprestimos)
            return True
        return False