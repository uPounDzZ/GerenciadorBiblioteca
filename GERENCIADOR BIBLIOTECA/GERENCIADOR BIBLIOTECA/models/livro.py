class Livro:
    def __init__(self, codigo, titulo, autor, ano, quantidade):
        self._codigo = codigo
        self._titulo = titulo
        self._autor = autor
        self._ano = ano
        self._quantidade = quantidade
        self._disponivel = quantidade
    
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def titulo(self):
        return self._titulo
    
    @property
    def autor(self):
        return self._autor
    
    @property
    def ano(self):
        return self._ano
    
    @property
    def quantidade(self):
        return self._quantidade
    
    @property
    def disponivel(self):
        return self._disponivel
    
    @disponivel.setter
    def disponivel(self, valor):
        self._disponivel = valor
    
    def __str__(self):
        return f"Código: {self._codigo} | Título: {self._titulo} | Autor: {self._autor} | Ano: {self._ano} | Disponível: {self._disponivel}/{self._quantidade}"