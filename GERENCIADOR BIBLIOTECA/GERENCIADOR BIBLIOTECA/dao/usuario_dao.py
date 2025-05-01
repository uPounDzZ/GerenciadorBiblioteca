import pickle
import os
from dao.abstract_dao import AbstractDAO

class UsuarioDAOMemoria(AbstractDAO):
    def __init__(self):
        self._usuarios = {}
    
    def salvar(self, usuario):
        self._usuarios[usuario.login] = usuario
        return usuario
    
    def buscar(self, login):
        return self._usuarios.get(login)
    
    def buscar_todos(self):
        return list(self._usuarios.values())
    
    def atualizar(self, usuario):
        if usuario.login in self._usuarios:
            self._usuarios[usuario.login] = usuario
            return usuario
        return None
    
    def deletar(self, login):
        if login in self._usuarios:
            del self._usuarios[login]
            return True
        return False

class UsuarioDAOArquivo(AbstractDAO):
    def __init__(self):
        self._arquivo = "usuarios.dat"
        if not os.path.exists(self._arquivo):
            with open(self._arquivo, 'wb') as f:
                pickle.dump({}, f)
    
    def _carregar(self):
        try:
            with open(self._arquivo, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    
    def _salvar_todos(self, usuarios):
        with open(self._arquivo, 'wb') as f:
            pickle.dump(usuarios, f)
    
    def salvar(self, usuario):
        usuarios = self._carregar()
        usuarios[usuario.login] = usuario
        self._salvar_todos(usuarios)
        return usuario
    
    def buscar(self, login):
        usuarios = self._carregar()
        return usuarios.get(login)
    
    def buscar_todos(self):
        usuarios = self._carregar()
        return list(usuarios.values())
    
    def atualizar(self, usuario):
        usuarios = self._carregar()
        if usuario.login in usuarios:
            usuarios[usuario.login] = usuario
            self._salvar_todos(usuarios)
            return usuario
        return None
    
    def deletar(self, login):
        usuarios = self._carregar()
        if login in usuarios:
            del usuarios[login]
            self._salvar_todos(usuarios)
            return True
        return False