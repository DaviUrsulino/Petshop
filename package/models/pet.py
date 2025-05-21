# Classe Pet representa o animal do cliente
class Pet:
    def __init__(self, nome, idade):
        self.nome = nome       # Validação no setter
        self.idade = idade     # Validação no setter

    @property
    def nome(self):
        return self._nome

    # Setter com validação: nome deve conter apenas letras e espaços
    @nome.setter
    def nome(self, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Nome do pet inválido.")
        self._nome = value

    @property
    def idade(self):
        return self._idade

    # Setter com validação: idade deve ser número inteiro
    @idade.setter
    def idade(self, value):
        if not str(value).isdigit():
            raise ValueError("Idade inválida.")
        self._idade = int(value)
