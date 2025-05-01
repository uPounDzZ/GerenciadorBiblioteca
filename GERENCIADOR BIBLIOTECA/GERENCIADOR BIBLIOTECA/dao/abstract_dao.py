from abc import ABC, abstractmethod

class AbstractDAO(ABC):
    @abstractmethod
    def salvar(self, obj):
        pass
    
    @abstractmethod
    def buscar(self, chave):
        pass
    
    @abstractmethod
    def buscar_todos(self):
        pass
    
    @abstractmethod
    def atualizar(self, obj):
        pass
    
    @abstractmethod
    def deletar(self, chave):
        pass