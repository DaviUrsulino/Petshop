# package/interface/janela.py

import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser

# Importa os modelos e lógicas do sistema
from package.models.cliente import Cliente
from package.models.pet import Pet
from package.models.servico import Banho, Tosa, Consulta
from package.services.agendamento import Agendamento
from package.utils.validacoes import validar_dados_formatos, validar_dados_temporais
from package.utils.arquivo_json import adicionar_agendamento, carregar_agendamentos, remover_agendamento

class JanelaPrincipal:
    """
    Classe da interface principal do Petshop.
    Permite agendar serviços para pets com envio via Telegram.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Petshop - Agendamento")
        self.root.geometry("500x580")
        self.root.configure(bg="#fff9f2")  # Fundo claro

        # Título da janela
        tk.Label(root, text="🐶 Agendamento de Serviços", bg="#fff9f2", fg="#3e2723",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Container para os campos
        frame = tk.Frame(root, bg="#fff9f2")
        frame.pack(pady=5)

        # Campos de entrada de dados
        self.nome_dono = tk.Entry(frame)     # Nome do dono
        self.nome_pet = tk.Entry(frame)      # Nome do pet
        self.idade_pet = tk.Entry(frame)     # Idade do pet
        self.data = tk.Entry(frame)          # Data do agendamento
        self.hora = tk.Entry(frame)          # Hora do agendamento

        # Labels correspondentes aos campos
        labels = ["Nome do Dono", "Nome do Pet", "Idade", "Data (dd/mm/aa)", "Hora (hh:mm)"]
        entradas = [self.nome_dono, self.nome_pet, self.idade_pet, self.data, self.hora]

        for i, (label, entry) in enumerate(zip(labels, entradas)):
            tk.Label(frame, text=label, bg="#fff9f2", font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky="w", padx=10, pady=4
            )
            entry.grid(row=i, column=1, padx=10)

        # Checkboxes para serviços
        self.var_banho = tk.BooleanVar()
        self.var_tosa = tk.BooleanVar()
        self.var_consulta = tk.BooleanVar()

        tk.Label(frame, text="Serviços:", bg="#fff9f2", font=("Arial", 10, "bold")).grid(
            row=5, column=0, sticky="w", padx=10
        )
        tk.Checkbutton(frame, text="Banho - R$40", variable=self.var_banho, bg="#fff9f2").grid(row=5, column=1, sticky="w")
        tk.Checkbutton(frame, text="Tosa - R$50", variable=self.var_tosa, bg="#fff9f2").grid(row=6, column=1, sticky="w")
        tk.Checkbutton(frame, text="Consulta - R$90", variable=self.var_consulta, bg="#fff9f2").grid(row=7, column=1, sticky="w")

        # Botão para agendar
        tk.Button(root, text="Agendar", command=self.agendar,
                  bg="#4caf50", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        # Botão para cancelar agendamento
        tk.Button(root, text="❌ Cancelar Selecionado", command=self.cancelar_agendamento,
                  bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(pady=2)

        # Lista para mostrar agendamentos
        self.lista = tk.Listbox(root, width=70, height=5)
        self.lista.pack(pady=5)

        # Link para abrir o bot do Telegram
        link_bot = tk.Label(root,
                            text="📱 Clique aqui para conversar com o bot do Telegram",
                            fg="blue", cursor="hand2", bg="#fff9f2", font=("Arial", 9, "italic"))
        link_bot.pack(pady=5)
        link_bot.bind("<Button-1>", lambda e: self.abrir_bot_telegram())

        # Mostrar os agendamentos existentes ao iniciar
        self.mostrar_agendamentos()

    def abrir_bot_telegram(self):
        """Abre o navegador com o link para o bot do Telegram."""
        webbrowser.open("https://t.me/PetshoTrabalho_bot")

    def detectar_chat_id(self):
        """Detecta o último chat_id que interagiu com o bot."""
        token = "7355084198:AAF7E7n46sx7NWbeZcrGIM3tOVpYaIN-c1g"
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados["result"]:
                return dados["result"][-1]["message"]["chat"]["id"]
        return None

    def agendar(self):
        """Realiza a validação dos dados, cria o agendamento e salva."""
        nome_dono = self.nome_dono.get().strip()
        nome_pet = self.nome_pet.get().strip()
        idade = self.idade_pet.get().strip()
        data = self.data.get().strip()
        hora = self.hora.get().strip()

        # Validações
        if not nome_dono.replace(" ", "").isalpha():
            messagebox.showerror("Erro", "Nome do dono inválido.")
            return
        if not nome_pet.replace(" ", "").isalpha():
            messagebox.showerror("Erro", "Nome do pet inválido.")
            return
        if not idade.isdigit():
            messagebox.showerror("Erro", "Idade inválida.")
            return
        if not validar_dados_formatos(data, hora):
            messagebox.showerror("Erro", "Formato inválido. Use dd/mm/aa e hh:mm.")
            return
        if not validar_dados_temporais(data, hora):
            messagebox.showerror("Erro", "Data ou hora inválida. Permitido das 08h às 18h e no futuro.")
            return

        # Seleciona os serviços marcados
        servicos = []
        if self.var_banho.get(): servicos.append(Banho())
        if self.var_tosa.get(): servicos.append(Tosa())
        if self.var_consulta.get(): servicos.append(Consulta())
        if not servicos:
            messagebox.showerror("Erro", "Selecione ao menos um serviço.")
            return

        # Tenta detectar o chat_id do Telegram
        chat_id = self.detectar_chat_id()
        if not chat_id:
            messagebox.showerror("Erro", "Chat ID não detectado.")
            return

        try:
            pet = Pet(nome_pet, idade)
            cliente = Cliente(nome_dono, pet)
            agendamento = Agendamento(cliente, data, hora, chat_id, servicos)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")
            return

        # Confirma e salva
        if agendamento.confirmar():
            adicionar_agendamento({
                "cliente": nome_dono,
                "pet": nome_pet,
                "idade": idade,
                "data": data,
                "hora": hora,
                "servicos": [s.nome for s in servicos]
            })
            messagebox.showinfo("Sucesso", "Agendamento enviado com sucesso!")
            self.limpar_campos()
            self.mostrar_agendamentos()
        else:
            messagebox.showerror("Erro", "Erro ao enviar agendamento.")

    def limpar_campos(self):
        """Limpa os campos após agendamento."""
        self.nome_dono.delete(0, tk.END)
        self.nome_pet.delete(0, tk.END)
        self.idade_pet.delete(0, tk.END)
        self.data.delete(0, tk.END)
        self.hora.delete(0, tk.END)
        self.var_banho.set(False)
        self.var_tosa.set(False)
        self.var_consulta.set(False)

    def mostrar_agendamentos(self):
        """Exibe todos os agendamentos salvos no listbox."""
        self.lista.delete(0, tk.END)
        for i, item in enumerate(carregar_agendamentos()):
            texto = f"{i+1}. {item['pet']} - {item['data']} às {item['hora']} ({', '.join(item['servicos'])})"
            self.lista.insert(tk.END, texto)

    def cancelar_agendamento(self):
        """Cancela o agendamento selecionado na lista."""
        selecao = self.lista.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um agendamento para cancelar.")
            return
        remover_agendamento(selecao[0])
        self.mostrar_agendamentos()
        messagebox.showinfo("Cancelado", "Agendamento cancelado com sucesso.")
