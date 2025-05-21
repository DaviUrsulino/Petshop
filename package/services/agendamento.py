# package/services/agendamento.py

from package.utils.telegram_bot import TelegramMixin         # Para envio real via Telegram
from package.utils.mixins import MensagemMixin               # Mixin auxiliar para confirmação local

# ✅ HERANÇA MÚLTIPLA com mixin
class Agendamento(MensagemMixin, TelegramMixin):
    """
    Classe responsável por criar e confirmar um agendamento de petshop.
    Herdando TelegramMixin e MensagemMixin para reutilização de funcionalidades.
    """

    def __init__(self, cliente, data, hora, chat_id, servicos):
        self.cliente = cliente                 # Associação fraca: Agendamento conhece Cliente
        self.data = data
        self.hora = hora
        self.chat_id = chat_id
        self.servicos = servicos              # Lista de objetos de serviço (herança + polimorfismo)
        self.preco_total = sum(s.preco for s in servicos)
        self.pontos_fidelidade = len(servicos) * 10  # Fidelidade: 10 pontos por serviço

    def confirmar(self):
        """
        Gera a mensagem de confirmação, envia via Telegram (método herdado) e chama o mixin auxiliar.
        """
        mensagem = self.gerar_mensagem()

        # ✅ Chama o mixin auxiliar (print local para simular envio ou log)
        self.enviar_confirmacao_local(mensagem)

        # ✅ Envia a mensagem real via Telegram (método herdado do TelegramMixin)
        return self.enviar_telegram(self.chat_id, mensagem)

    def gerar_mensagem(self):
        """
        Monta a mensagem de confirmação com todos os dados do agendamento.
        """
        return (f"🐾 Agendamento Confirmado!\n"
                f"Cliente: {self.cliente.nome}\n"
                f"Pet: {self.cliente.pet.nome} ({self.cliente.pet.idade} anos)\n"
                f"Serviços: {', '.join([s.nome for s in self.servicos])}\n"
                f"Data: {self.data} às {self.hora}\n"
                f"Valor total: R$ {self.preco_total:.2f}\n"
                f"🎁 Pontos de fidelidade: {self.pontos_fidelidade}")
