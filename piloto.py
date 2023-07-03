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

        # get driver id
        c.execute(
            """ SELECT DriverId 
                FROM Driver 
                WHERE Forename = %s AND Surname = %s""",
                (forename, surname,))
        driver_id = c.fetchone()[0]

        # Consulta para obter a quantidade de vitórias do piloto
        c.callproc('quant_vitorias_piloto',(driver_id,))
        victory_count = c.fetchone()[0]

        #  Primeiro e último ano em que há dados
        #  do piloto na base (pela tabela RESULTS).
        c.callproc('primeiro_ultimo_ano_piloto',(driver_id,))
        first_year, last_year = c.fetchone()

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
        c.callproc("vitorias_piloto_relatorio5", (piloto_id,)) 
        data = c.fetchall()

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = ('Ano','NomeCorrida','Quantidade')

        tree.column("Ano", width=100)
        tree.heading("Ano", text="Ano")

        tree.column("NomeCorrida", width=300)
        tree.heading("NomeCorrida", text="NomeCorrida")

        tree.column("Quantidade", width=100)
        tree.heading("Quantidade", text="Quantidade")

        for row in data:
            tree.insert('', 'end', values=row)
        tree.pack()

# Define a janela que exibe o relatório de resultados por status do piloto
class ReportResultsFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.city_label = tk.Label(self, text="Relatório de Listagem de Resultados por Status")
        self.city_label.pack(pady=20)

        self.create_table()
        
        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.back_button.pack(side="bottom", pady=20)

    def create_table(self):
        piloto_id = get_piloto_id(self.username)
        
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.callproc("status_das_corridas_do_piloto_relatorio6",(piloto_id,))

        data = c.fetchall()

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = ("Status","Quantidade")

        tree.column("Status", width=200)
        tree.heading("Status", text="Status")

        tree.column("Quantidade", width=100)
        tree.heading("Quantidade", text="Quantidade")

        for row in data:
            tree.insert('', 'end', values=row)

        tree.pack()