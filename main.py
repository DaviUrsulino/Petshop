import sys
import os

# Adiciona o caminho absoluto da pasta onde está o main.py ao sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from package.interface.janela import JanelaPrincipal
import tkinter as tk

# Inicia a aplicação com a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaPrincipal(root)
    root.mainloop()
