from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self, codigo, usuario, livro, data_emprestimo=None):
        self._codigo = codigo
        self._usuario = usuario
        self._livro = livro
        self._data_emprestimo = data_emprestimo if data_emprestimo else datetime.now()
        self._data_devolucao_prevista = self._data_emprestimo + timedelta(days=15)
        self._data_devolucao_real = None
        self._status = "Ativo"
    
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def livro(self):
        return self._livro
    
    @property
    def data_emprestimo(self):
        return self._data_emprestimo
    
    @property
    def data_devolucao_prevista(self):
        return self._data_devolucao_prevista
    
    @property
    def data_devolucao_real(self):
        return self._data_devolucao_real
    
    @property
    def status(self):
        return self._status
    
    def devolver(self):
        self._data_devolucao_real = datetime.now()
        self._status = "Devolvido"
    
    def __str__(self):
        return f"Empréstimo: {self._codigo} | Usuário: {self._usuario.login} | Livro: {self._livro.titulo} | Status: {self._status}"