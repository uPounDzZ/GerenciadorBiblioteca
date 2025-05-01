from business.relatorios.relatorio_template import RelatorioTemplate
from collections import defaultdict

class RelatorioEmprestimos(RelatorioTemplate):
    def _criar_cabecalho(self):
        return "=== RELATÓRIO DE EMPRÉSTIMOS ==="
    
    def _processar_dados(self, emprestimos):
        if not emprestimos:
            return "Nenhum empréstimo registrado."
        
        # Estatísticas de empréstimos
        total_emprestimos = len(emprestimos)
        emprestimos_ativos = len([e for e in emprestimos if e.status == "Ativo"])
        emprestimos_devolvidos = len([e for e in emprestimos if e.status == "Devolvido"])
        
        # Estatísticas por usuário
        emprestimos_por_usuario = defaultdict(int)
        for emprestimo in emprestimos:
            emprestimos_por_usuario[emprestimo.usuario.login] += 1
        
        # Estatísticas por livro
        emprestimos_por_livro = defaultdict(int)
        for emprestimo in emprestimos:
            emprestimos_por_livro[emprestimo.livro.titulo] += 1
        
        resultado = []
        resultado.append(f"Total de empréstimos: {total_emprestimos}")
        resultado.append(f"Empréstimos ativos: {emprestimos_ativos}")
        resultado.append(f"Empréstimos devolvidos: {emprestimos_devolvidos}")
        
        resultado.append("\nTop usuários por número de empréstimos:")
        for i, (usuario, count) in enumerate(sorted(emprestimos_por_usuario.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            resultado.append(f"{i}. {usuario} - {count} empréstimo(s)")
        
        resultado.append("\nTop livros mais emprestados:")
        for i, (livro, count) in enumerate(sorted(emprestimos_por_livro.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            resultado.append(f"{i}. {livro} - {count} empréstimo(s)")
        
        return "\n".join(resultado)