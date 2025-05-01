class Memento:
    """Classe para armazenar o estado de um objeto"""
    
    def __init__(self, estado):
        self._estado = estado
    
    def get_estado(self):
        return self._estado