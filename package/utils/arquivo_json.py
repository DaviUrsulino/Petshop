import json
import os

# Caminho do arquivo de agendamentos
ARQUIVO = "agendamentos.json"

def carregar_agendamentos():
    """"""""""
    Lê o arquivo JSON de agendamentos e retorna como lista de dicionários.
    Se o arquivo não existir, cria um novo com lista vazia.
    """
    if not os.path.exists(ARQUIVO):
        salvar_agendamentos([])
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_agendamentos(lista):
    """
    Salva a lista de agendamentos no arquivo JSON com identação.
    """
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def adicionar_agendamento(agendamento):
    """
    Adiciona um novo agendamento à lista existente e salva no arquivo.
    """
    lista = carregar_agendamentos()
    lista.append(agendamento)
    salvar_agendamentos(lista)

def remover_agendamento(indice):
    """
    Remove o agendamento da lista com base no índice e salva novamente o arquivo.
    """
    lista = carregar_agendamentos()
    if 0 <= indice < len(lista):
        lista.pop(indice)
        salvar_agendamentos(lista)
