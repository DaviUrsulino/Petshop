import requests

class TelegramMixin:
    def enviar_telegram(self, chat_id, mensagem):
        token = "7355084198:AAF7E7n46sx7NWbeZcrGIM3tOVpYaIN-c1g"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": mensagem}
        response = requests.post(url, data=data)
        return response.status_code == 200
