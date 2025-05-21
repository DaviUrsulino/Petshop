from datetime import datetime

# Valida se data e hora estão nos formatos corretos
def validar_dados_formatos(data, hora):
    try:
        datetime.strptime(data, "%d/%m/%y")
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

# Verifica se data e hora estão no futuro e entre 08h e 18h
def validar_dados_temporais(data, hora):
    try:
        data_obj = datetime.strptime(data, "%d/%m/%y")
        hora_obj = datetime.strptime(hora, "%H:%M").time()
        agora = datetime.now()

        if data_obj.date() < agora.date():
            return False
        if data_obj.date() == agora.date() and hora_obj < agora.time():
            return False
        if not (8 <= hora_obj.hour < 18):
            return False
        return True
    except:
        return False
