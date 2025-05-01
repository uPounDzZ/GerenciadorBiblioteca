from abc import ABC, abstractmethod

class Comando(ABC):
    """Interface para o padrão Command"""
    
    @abstractmethod
    def executar(self):
        pass

class Invoker:
    """Invocador para o padrão Command"""
    
    def __init__(self):
        self._historico = []
    
    def executar(self, comando):
        resultado = comando.executar()
        self._historico.append(comando)
        return resultado
    
    def get_historico(self):
        return self._historico