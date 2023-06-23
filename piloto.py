import tkinter as tk
from tkinter import ttk

# Define a janela exibida após o login bem-sucedido para Piloto
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=f"Olá, piloto {username}!")
        self.label.pack()

        self.button = tk.Button(self, text="Ir para a Tela 3", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.button.pack()

        self.logout_button = tk.Button(self, text="Sair", command=self.logout)
        self.logout_button.pack(side="bottom", pady=50)

    def logout(self):
        self.master.switch_frame(self.master.login_frame)

# Define a janela que exibe os dados buscados do banco de dados para Piloto
class ReportFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        # código específico do Piloto aqui
