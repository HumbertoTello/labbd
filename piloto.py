import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2.extras import DictCursor
import configparser

# Função que conecta com o banco de dados
def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['postgresql']

# Função para pegar o nome do piloto
def get_piloto_name(username):
    db_config = get_config()  # a função get_config deve retornar um dicionário com as configurações do banco de dados
    conn = psycopg2.connect(**db_config)
    c = conn.cursor(cursor_factory=DictCursor)

    c.execute("""SELECT Driver.Forename || ' ' || Driver.Surname AS Name 
                FROM Driver
                INNER JOIN users
                ON Driver.DriverId = users.IdOriginal
                WHERE users.Login = %s;""", (username,))

    name = c.fetchone()[0]
    c.close()
    conn.close()

    return name

# Função para pegar o id do piloto
def get_piloto_id(username):
    db_config = get_config()  # a função get_config deve retornar um dicionário com as configurações do banco de dados
    conn = psycopg2.connect(**db_config)
    c = conn.cursor()

    c.execute("""SELECT IdOriginal 
                FROM users
                WHERE Login = %s;""", (username,))

    piloto_id = c.fetchone()[0]
    c.close()
    conn.close()

    return piloto_id

# Define a janela exibida após o login bem-sucedido para piloto
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        piloto_name = get_piloto_name(username)
        forename, surname = piloto_name.split(' ')
        self.label = tk.Label(self, text=f"Olá, piloto {piloto_name}!")
        self.label.pack(pady=10)

        # Obtém as informações sobre o piloto
        victory_count, first_year, last_year = self.get_piloto_info(forename, surname)

        self.victories_label = tk.Label(self, text=f"Quantidade de vitórias: {victory_count}")
        self.victories_label.pack()

        self.first_year_label = tk.Label(self, text=f"Primeiro ano de dados: {first_year}")
        self.first_year_label.pack()

        self.last_year_label = tk.Label(self, text=f"Último ano de dados: {last_year}")
        self.last_year_label.pack(pady=(0, 10))

        self.button = tk.Button(self, text="Acessar Relatórios", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.button.pack()

        self.logout_button = tk.Button(self, text="Sair", command=self.logout)
        self.logout_button.pack(side="bottom", pady=50)
    
    def logout(self):
        self.master.switch_frame(self.master.login_frame)

    def get_piloto_info(self, forename, surname):
        # Conecta ao banco de dados e obtém as informações sobre o piloto
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        # Consulta para obter a quantidade de vitórias do piloto
        c.execute("""SELECT COUNT(*) 
             FROM Results 
             WHERE DriverId = (SELECT DriverId 
                               FROM Driver 
                               WHERE Forename = %s AND Surname = %s) 
             AND Position = 1""", (forename, surname,))
        victory_count = c.fetchone()[0]

        # Consulta para obter o primeiro ano em que há dados do piloto na base
        # c.execute("INSERIR A QUERY AQUI", (forename, surname,))
        # first_year = c.fetchone()[0]
        first_year = 0 # Inserir a query, descomentar o código acima e deletar essa linha

        # Consulta para obter o último ano em que há dados do piloto na base
        # c.execute("INSERIR A QUERY AQUI", (forename, surname,))
        # last_year = c.fetchone()[0]
        last_year = 0 # Inserir a query, descomentar o código acima e deletar essa linha

        conn.close()

        return victory_count, first_year, last_year

# Define a janela que exibe os dados buscados do banco de dados para o piloto
class ReportFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.label = tk.Label(self, text="Relatórios de Piloto")
        self.label.pack(pady=20)

        self.drivers_button = tk.Button(self, text="Relatório de Listagem de Vitórias", command=lambda: self.master.switch_frame(ReportWinsFrame(self.master, username)))
        self.drivers_button.pack()

        self.airports_button = tk.Button(self, text="Relatório de Resultados por Status", command=lambda: self.master.switch_frame(ReportResultsFrame(self.master, username)))
        self.airports_button.pack()

        self.results_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(LoginSuccessFrame(self.master, username)))
        self.results_button.pack(side="bottom", pady=20)

# Define a janela que exibe o relatório de lista de vitórias do piloto
class ReportWinsFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.city_label = tk.Label(self, text="Relatório de Listagem de Vitórias do Piloto")
        self.city_label.pack(pady=20)

        self.create_table()
        
        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.back_button.pack(side="bottom", pady=20)

    def create_table(self):
        piloto_id = get_piloto_id(self.username)
        
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT * FROM driver WHERE driverid = %s", (piloto_id,)) # Inserir a query correta aqui

        data = c.fetchall()

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = ("Coluna 1", "Coluna 2", "Coluna 3", "Coluna 4", "Coluna 5", "Coluna 6", "Coluna 7", "Coluna 8")

        tree.column("Coluna 1", width=100)
        tree.heading("Coluna 1", text="Coluna 1")

        tree.column("Coluna 2", width=100)
        tree.heading("Coluna 2", text="Coluna 2")

        tree.column("Coluna 3", width=100)
        tree.heading("Coluna 3", text="Coluna 3")

        tree.column("Coluna 4", width=100)
        tree.heading("Coluna 4", text="Coluna 4")

        tree.column("Coluna 5", width=100)
        tree.heading("Coluna 5", text="Coluna 5")

        tree.column("Coluna 6", width=100)
        tree.heading("Coluna 6", text="Coluna 6")

        tree.column("Coluna 7", width=100)
        tree.heading("Coluna 7", text="Coluna 7")

        tree.column("Coluna 8", width=100)
        tree.heading("Coluna 8", text="Coluna 8")

        for row in data:
            tree.insert('', 'end', values=row)

        tree.pack()

# Define a janela que exibe o relatório de resultados por status do piloto
class ReportResultsFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.city_label = tk.Label(self, text="Relatório de Listagem de Vitórias do Piloto")
        self.city_label.pack(pady=20)

        self.create_table()
        
        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.back_button.pack(side="bottom", pady=20)

    def create_table(self):
        piloto_id = get_piloto_id(self.username)
        
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT * FROM driver WHERE driverid = %s", (piloto_id,)) # Inserir a query correta aqui

        data = c.fetchall()

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = ("Coluna 1", "Coluna 2", "Coluna 3", "Coluna 4", "Coluna 5", "Coluna 6", "Coluna 7", "Coluna 8")

        tree.column("Coluna 1", width=100)
        tree.heading("Coluna 1", text="Coluna 1")

        tree.column("Coluna 2", width=100)
        tree.heading("Coluna 2", text="Coluna 2")

        tree.column("Coluna 3", width=100)
        tree.heading("Coluna 3", text="Coluna 3")

        tree.column("Coluna 4", width=100)
        tree.heading("Coluna 4", text="Coluna 4")

        tree.column("Coluna 5", width=100)
        tree.heading("Coluna 5", text="Coluna 5")

        tree.column("Coluna 6", width=100)
        tree.heading("Coluna 6", text="Coluna 6")

        tree.column("Coluna 7", width=100)
        tree.heading("Coluna 7", text="Coluna 7")

        tree.column("Coluna 8", width=100)
        tree.heading("Coluna 8", text="Coluna 8")

        for row in data:
            tree.insert('', 'end', values=row)

        tree.pack()