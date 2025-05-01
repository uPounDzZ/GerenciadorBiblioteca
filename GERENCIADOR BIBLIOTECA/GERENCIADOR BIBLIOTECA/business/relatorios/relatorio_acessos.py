from business.relatorios.relatorio_template import RelatorioTemplate

class RelatorioAcessos(RelatorioTemplate):
    def _criar_cabecalho(self):
        return "=== RELATÓRIO DE ACESSOS DOS USUÁRIOS ==="
    
    def _processar_dados(self, usuarios):
        if not usuarios:
            return "Nenhum usuário cadastrado."
        
        # Ordenar usuários por número de acessos (decrescente)
        usuarios_ordenados = sorted(usuarios, key=lambda u: u.acessos, reverse=True)
        
        # Calcular estatísticas
        total_usuarios = len(usuarios)
        total_acessos = sum(u.acessos for u in usuarios)
        media_acessos = total_acessos / total_usuarios if total_usuarios > 0 else 0
        
        resultado = []
        resultado.append(f"Total de usuários: {total_usuarios}")
        resultado.append(f"Total de acessos: {total_acessos}")
        resultado.append(f"Média de acessos por usuário: {media_acessos:.2f}")
        resultado.append("\nDetalhamento de acessos por usuário:")
        
        for i, usuario in enumerate(usuarios_ordenados, 1):
            resultado.append(f"{i}. {usuario.login} - {usuario.acessos} acesso(s) - {'Admin' if usuario.admin else 'Usuário comum'}")
        
        return "\n".join(resultado)