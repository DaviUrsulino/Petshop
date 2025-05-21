# Este mixin serve apenas para demonstrar polimorfismo/herança múltipla
# Ele apenas imprime uma mensagem simulando o envio local

class MensagemMixin:
    def enviar_confirmacao_local(self, mensagem):
        print(f"[MIXIN] Mensagem de confirmação local:\n{mensagem}\n")
