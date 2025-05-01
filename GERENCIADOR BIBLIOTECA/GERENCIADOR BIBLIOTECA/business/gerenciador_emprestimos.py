from models.emprestimo import Emprestimo
from business.relatorios.relatorio_emprestimos import RelatorioEmprestimos

class GerenciadorEmprestimos:
    def __init__(self, emprestimo_dao):
        self._emprestimo_dao = emprestimo_dao
    
    def realizar(self, codigo, usuario, livro):
        if self.buscar(codigo):
            raise ValueError(f"Empréstimo com código '{codigo}' já existe")
        
        emprestimo = Emprestimo(codigo, usuario, livro)
        return self._emprestimo_dao.salvar(emprestimo)
    
    def devolver(self, codigo):
        emprestimo = self.buscar(codigo)
        if not emprestimo:
            raise ValueError(f"Empréstimo com código '{codigo}' não encontrado")
        
        emprestimo.devolver()
        return self._emprestimo_dao.atualizar(emprestimo)
    
    def buscar(self, codigo):
        return self._emprestimo_dao.buscar(codigo)
    
    def buscar_todos(self):
        return self._emprestimo_dao.buscar_todos()
    
    def buscar_por_usuario(self, login_usuario):
        emprestimos = self.buscar_todos()
        return [e for e in emprestimos if e.usuario.login == login_usuario]
    
    def gerar_relatorio_emprestimos(self):
        relatorio = RelatorioEmprestimos()
        return relatorio.gerar(self.buscar_todos())