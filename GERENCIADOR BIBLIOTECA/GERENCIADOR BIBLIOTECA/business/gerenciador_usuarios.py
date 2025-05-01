from models.usuario import Usuario
from util.exceptions import LoginInvalido, SenhaInvalida
from util.memento import Memento
import re
from business.relatorios.relatorio_acessos import RelatorioAcessos

class GerenciadorUsuarios:
    def __init__(self, usuario_dao):
        self._usuario_dao = usuario_dao
        self._mementos = {}
    
    def cadastrar(self, login, senha, admin=False):
        self._validar_login(login)
        self._validar_senha(senha)
        
        if self.buscar(login):
            raise ValueError(f"Usuário com login '{login}' já existe")
        
        usuario = Usuario(login, senha, admin)
        return self._usuario_dao.salvar(usuario)
    
    def buscar(self, login):
        return self._usuario_dao.buscar(login)
    
    def buscar_todos(self):
        return self._usuario_dao.buscar_todos()
    
    def atualizar(self, login, senha, admin):
        usuario = self.buscar(login)
        if not usuario:
            raise ValueError(f"Usuário com login '{login}' não encontrado")
        
        self._salvar_memento(usuario)
        
        self._validar_senha(senha)
        usuario = Usuario(login, senha, admin)
        return self._usuario_dao.atualizar(usuario)
    
    def deletar(self, login):
        usuario = self.buscar(login)
        if not usuario:
            raise ValueError(f"Usuário com login '{login}' não encontrado")
        
        return self._usuario_dao.deletar(login)
    
    def autenticar(self, login, senha):
        usuario = self.buscar(login)
        if not usuario:
            return None
        
        if usuario.senha != senha:
            return None

        usuario.incrementar_acesso()
        self._usuario_dao.atualizar(usuario)
        
        return usuario
    
    def _validar_login(self, login):
        if not login:
            raise LoginInvalido("Login não pode ser vazio")
        
        if len(login) > 12:
            raise LoginInvalido("Login deve ter no máximo 12 caracteres")
        
        if re.search(r'\d', login):
            raise LoginInvalido("Login não pode conter números")
    
    def _validar_senha(self, senha):
        
        if len(senha) < 8:
            raise SenhaInvalida("Senha deve ter pelo menos 8 caracteres")
        
        if not re.search(r'[a-z]', senha):
            raise SenhaInvalida("Senha deve conter pelo menos uma letra minúscula")
        
        if not re.search(r'[A-Z]', senha):
            raise SenhaInvalida("Senha deve conter pelo menos uma letra maiúscula")
        
        if not re.search(r'\d', senha):
            raise SenhaInvalida("Senha deve conter pelo menos um número")
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"|,.<>/?]', senha):
            raise SenhaInvalida("Senha deve conter pelo menos um caractere especial")
    
    def _salvar_memento(self, usuario):
        self._mementos[usuario.login] = Memento(Usuario(usuario.login, usuario.senha, usuario.admin))
    
    def restaurar_memento(self, login=None):
        if login is None:
            if not self._mementos:
                raise ValueError("Não há estado anterior para restaurar")
            
            ultimo_login = list(self._mementos.keys())[-1]
            return self.restaurar_memento(ultimo_login)
        
        if login not in self._mementos:
            raise ValueError(f"Não há estado anterior para o usuário '{login}'")
        
        estado_anterior = self._mementos[login].get_estado()
        self._usuario_dao.atualizar(estado_anterior)
        del self._mementos[login]
        return estado_anterior
    
    def gerar_relatorio_acessos(self):
        relatorio = RelatorioAcessos()
        return relatorio.gerar(self.buscar_todos())