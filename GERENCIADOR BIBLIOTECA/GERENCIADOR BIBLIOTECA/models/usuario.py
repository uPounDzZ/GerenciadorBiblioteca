class Usuario:
    def __init__(self, login, senha, admin=False):
        self._login = login
        self._senha = senha
        self._admin = admin
        self._acessos = 0
    
    @property
    def login(self):
        return self._login
    
    @property
    def senha(self):
        return self._senha
    
    @property
    def admin(self):
        return self._admin
    
    @property
    def acessos(self):
        return self._acessos
    
    def incrementar_acesso(self):
        self._acessos += 1
    
    def __str__(self):
        return f"Usuário: {self._login} | Admin: {'Sim' if self._admin else 'Não'} | Acessos: {self._acessos}"