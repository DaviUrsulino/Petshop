# Classe Cliente representa o dono do pet
class Cliente:
    def __init__(self, nome, pet):
        self.nome = nome        # Atribui nome com validação (via setter)
        self.pet = pet          # Atribui pet com validação (via setter)

    # Getter do nome
    @property
    def nome(self):
        return self._nome

    # Setter do nome com validação: só letras e espaços
    @nome.setter
    def nome(self, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Nome do cliente inválido.")
        self._nome = value

    # Getter do pet
    @property
    def pet(self):
        return self._pet

    # Setter do pet (sem validação pois já é instância de Pet)
    @pet.setter
    def pet(self, value):
        self._pet = value
