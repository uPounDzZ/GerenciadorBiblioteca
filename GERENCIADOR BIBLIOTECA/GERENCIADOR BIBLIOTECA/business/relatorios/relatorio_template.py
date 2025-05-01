from abc import ABC, abstractmethod

# Template Method para relatórios
class RelatorioTemplate(ABC):
    def gerar(self, dados):
        """Template method que define o esqueleto do algoritmo de geração de relatório"""
        cabecalho = self._criar_cabecalho()
        corpo = self._processar_dados(dados)
        rodape = self._criar_rodape()
        
        return f"{cabecalho}\n\n{corpo}\n\n{rodape}"
    
    @abstractmethod
    def _criar_cabecalho(self):
        """Cria o cabeçalho do relatório"""
        pass
    
    @abstractmethod
    def _processar_dados(self, dados):
        """Processa os dados do relatório"""
        pass
    
    def _criar_rodape(self):
        """Cria o rodapé do relatório"""
        from datetime import datetime
        return f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"