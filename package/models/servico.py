# Classe base Servico usando encapsulamento
class Servico:
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    @property
    def nome(self):
        return self._nome

    @property
    def preco(self):
        return self._preco

# Herança para serviços específicos com preços definidos
class Banho(Servico):
    def __init__(self):
        super().__init__("Banho", 40.0)

class Tosa(Servico):
    def __init__(self):
        super().__init__("Tosa", 50.0)

class Consulta(Servico):
    def __init__(self):
        super().__init__("Consulta", 90.0)
