import tkinter as tk
from tkinter import ttk

# Define a janela exibida após o login bem-sucedido para Admin
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=f"Olá, Admin!")
        self.label.pack()

        self.button = tk.Button(self, text="Ir para a Tela 3", command=lambda: self.master.switch_frame(ThirdFrame))
        self.button.pack()

# Define a janela que exibe os dados buscados do banco de dados para Admin
class ThirdFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # código específico do Admin aqui
