import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2.extras import DictCursor
import configparser

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['postgresql']

def get_escuderia_name(username):
    db_config = get_config()  # a função get_config deve retornar um dicionário com as configurações do banco de dados
    conn = psycopg2.connect(**db_config)
    c = conn.cursor(cursor_factory=DictCursor)

    c.execute("""SELECT Constructors.Name 
                FROM Constructors
                INNER JOIN users
                ON Constructors.ConstructorId = users.IdOriginal
                WHERE users.Login = %s;""", (username,))

    name = c.fetchone()[0]
    c.close()
    conn.close()

    return name

# Define a janela exibida após o login bem-sucedido para Escuderia
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        escuderia_name = get_escuderia_name(username)
        self.label = tk.Label(self, text=f"Olá, escuderia {escuderia_name}!")
        self.label.pack(pady=10)

        # Obtém as informações sobre a escuderia
        victory_count, different_pilots, first_year, last_year = self.get_escuderia_info(escuderia_name)

        self.victories_label = tk.Label(self, text=f"Quantidade de vitórias: {victory_count}")
        self.victories_label.pack()

        self.pilots_label = tk.Label(self, text=f"Quantidade de pilotos: {different_pilots}")
        self.pilots_label.pack()

        self.first_year_label = tk.Label(self, text=f"Primeiro ano de dados: {first_year}")
        self.first_year_label.pack()

        self.last_year_label = tk.Label(self, text=f"Último ano de dados: {last_year}")
        self.last_year_label.pack(pady=(0, 10))

        self.button = tk.Button(self, text="Acessar Relatórios", command=lambda: self.master.switch_frame(ReportFrame))
        self.button.pack()

    def get_escuderia_info(self, escuderia_name):
        # Conecta ao banco de dados e obtém as informações sobre a escuderia
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        # Consulta para obter a quantidade de vitórias da escuderia
        c.execute("SELECT COUNT(*) FROM Results WHERE ConstructorId = (SELECT ConstructorId FROM Constructors WHERE Name = %s) AND Position = 1", (escuderia_name,))
        victory_count = c.fetchone()[0]

        # Consulta para obter a quantidade de pilotos diferentes que já correram pela escuderia
        # c.execute("INSERIR A QUERY AQUI", (escuderia_name,))
        # different_pilots = c.fetchone()[0]
        different_pilots = 0 # Inserir a query, descomentar o código acima e deletar essa linha

        # Consulta para obter o primeiro ano em que há dados da escuderia na base
        # c.execute("INSERIR A QUERY AQUI", (escuderia_name,))
        # first_year = c.fetchone()[0]
        first_year = 0 # Inserir a query, descomentar o código acima e deletar essa linha

        # Consulta para obter o último ano em que há dados da escuderia na base
        # c.execute("INSERIR A QUERY AQUI", (escuderia_name,))
        # last_year = c.fetchone()[0]
        last_year = 0 # Inserir a query, descomentar o código acima e deletar essa linha

        conn.close()

        return victory_count, different_pilots, first_year, last_year

# Define a janela que exibe os dados buscados do banco de dados para Escuderia
class ReportFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # código específico da Escuderia aqui
