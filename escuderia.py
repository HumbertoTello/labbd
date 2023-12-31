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

# Função para pegar o nome da escuderia
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

# Função para pegar o id da escuderia
def get_escuderia_id(username):
    db_config = get_config()  # a função get_config deve retornar um dicionário com as configurações do banco de dados
    conn = psycopg2.connect(**db_config)
    c = conn.cursor()

    c.execute("""SELECT IdOriginal 
                FROM users
                WHERE Login = %s AND Tipo = 'Escuderia';""", (username,))

    escuderia_id = c.fetchone()[0]
    c.close()
    conn.close()

    return escuderia_id

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

        self.query_button = tk.Button(self, text="Consulta por Primeiro Nome", command=lambda: self.master.switch_frame(SearchByFirstName(self.master, username)))
        self.query_button.pack(pady=10)

        self.button = tk.Button(self, text="Acessar Relatórios", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.button.pack()

        self.logout_button = tk.Button(self, text="Sair", command=self.logout)
        self.logout_button.pack(side="bottom", pady=50)
    
    def logout(self):
        self.master.switch_frame(self.master.login_frame)

    def get_escuderia_info(self, escuderia_name):
        # Conecta ao banco de dados e obtém as informações sobre a escuderia
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        # adquirir id da escuderia
        c.execute("""
            SELECT ConstructorId 
            FROM Constructors 
            WHERE Name = %s;
        """,(escuderia_name,))
        escuderia_id = c.fetchone()[0]

        # Consulta para obter a quantidade de vitórias da escuderia
        c.callproc('quant_vitorias_escuderia',(escuderia_id,))
        victory_count = c.fetchone()[0]

        # Consulta para obter a quantidade de pilotos diferentes que já correram pela escuderia
        c.callproc('quant_pilotos_diferentes',(escuderia_id,))
        different_pilots = c.fetchone()[0]

        # Consulta para obter o primeiro e ultimo ano em que há dados da escuderia na base
        c.callproc('primeiro_ultimo_ano_escuderia',(escuderia_id,))
        first_year,last_year = c.fetchone() # must unpack 2 values
        conn.close()

        return victory_count, different_pilots, first_year, last_year

# Define a janela que exibe a consulta por Primeiro Nome
class SearchByFirstName(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.label = tk.Label(self, text="Consulta por Primeiro Nome")
        self.label.pack(pady=20)

        self.first_name_label = tk.Label(self, text="Insira o primeiro nome de um piloto")
        self.first_name_label.pack(pady=10)

        self.first_name = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.first_name)
        self.entry.pack()

        self.submit_button = tk.Button(self, text="Consultar", command=self.create_table)
        self.submit_button.pack(pady=5)

        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(LoginSuccessFrame(self.master, username)))
        self.back_button.pack(side="bottom", pady=20)

        self.tree = None
    
    def get_pilots_by_escuderia(self, escuderia_name, forename):
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor(cursor_factory=DictCursor)

        c.execute("""SELECT DISTINCT D.Forename || ' ' || D.Surname AS complete_name, D.Dob, D.Nationality 
                     FROM Driver AS D
                     INNER JOIN Results AS R ON R.DriverId = D.DriverId
                     INNER JOIN Constructors AS C ON C.ConstructorId = R.ConstructorId
                     WHERE lower(C.Name) = lower(%s) AND 
                     lower(D.Forename) = lower(%s);
                  """, (escuderia_name, forename,))

        pilots = c.fetchall()
        c.close()
        conn.close()

        return pilots

    def create_table(self):
        if self.tree is not None:
            self.tree.destroy()

        # Chama a função get_escuderia_name para obter o nome da escuderia
        escuderia_name = get_escuderia_name(self.username)

        # Chama a função get_pilots_by_escuderia para obter os pilotos
        pilots = self.get_pilots_by_escuderia(escuderia_name, self.first_name.get())

        self.tree = ttk.Treeview(self, show='headings')
        self.tree["columns"] = ("Nome Completo", "Data de Nascimento", "Nacionalidade")

        self.tree.column("Nome Completo", width=200)
        self.tree.heading("Nome Completo", text="Nome Completo")

        self.tree.column("Data de Nascimento", width=200)
        self.tree.heading("Data de Nascimento", text="Data de Nascimento")

        self.tree.column("Nacionalidade", width=200)
        self.tree.heading("Nacionalidade", text="Nacionalidade")

        for pilot in pilots:
            self.tree.insert('', 'end', values=(pilot['complete_name'], pilot['dob'], pilot['nationality']))

        self.tree.pack()

# Define a janela que exibe os dados buscados do banco de dados para Escuderia
class ReportFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.label = tk.Label(self, text="Relatórios de Escuderia")
        self.label.pack(pady=20)

        self.drivers_button = tk.Button(self, text="Relatório de Listagem de Pilotos da Escuderia", command=lambda: self.master.switch_frame(ReportDriversFrame(self.master, username)))
        self.drivers_button.pack()

        self.airports_button = tk.Button(self, text="Relatório de Resultados por Status", command=lambda: self.master.switch_frame(ReportResultsFrame(self.master, username)))
        self.airports_button.pack()

        self.results_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(LoginSuccessFrame(self.master, username)))
        self.results_button.pack(side="bottom", pady=20)

# Define a janela que exibe o relatório de lista de pilotos da escuderia
class ReportDriversFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.username = username

        self.city_label = tk.Label(self, text="Relatório de Listagem de Pilotos da Escuderia")
        self.city_label.pack(pady=20)

        self.create_table()
        
        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(ReportFrame(self.master, username)))
        self.back_button.pack(side="bottom", pady=20)

    def create_table(self):
        escuderia_id = get_escuderia_id(self.username)

        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()


        c.callproc("pilotos_por_escuderia_rel_3", (escuderia_id,)) 
        data = c.fetchall()

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = ("Nome","Vitorias")

        tree.column("Nome", width=200)
        tree.heading("Nome", text="Nome")

        tree.column("Vitorias", width=100)
        tree.heading("Vitorias", text="Vitorias")

        for row in data:
            tree.insert('', 'end', values=row)

        tree.pack()

# Define a janela que exibe o relatório de resultados por status da escuderia
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
        escuderia_id = get_escuderia_id(self.username)

        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.callproc("status_por_escuderia_rel_4", (escuderia_id,))
        data = c.fetchall()

        tree = ttk.Treeview(self, show='headings')
        tree["columns"] = ("Status", "Quantidade")

        tree.column("Status", width=200)
        tree.heading("Status", text="Status")

        tree.column("Quantidade", width=100)
        tree.heading("Quantidade", text="Quantidade")

        for row in data:
            tree.insert('', 'end', values=row)

        tree.pack()