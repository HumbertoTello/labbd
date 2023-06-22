import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import configparser

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['postgresql']

# Define a janela exibida após o login bem-sucedido para Admin
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=f"Olá, Admin!")
        self.label.pack()

        # Obtém a quantidade de pilotos cadastrados
        pilot_count = self.get_pilot_count()  # Substitua com a função apropriada
        self.pilots_label = tk.Label(self, text=f"Pilotos cadastrados: {pilot_count}")
        self.pilots_label.pack()

        # Obtém a quantidade de escuderias cadastradas
        constructor_count = self.get_constructor_count()  # Substitua com a função apropriada
        self.constructors_label = tk.Label(self, text=f"Escuderias cadastradas: {constructor_count}")
        self.constructors_label.pack()

        # Obtém a quantidade de corridas cadastradas
        race_count = self.get_race_count()  # Substitua com a função apropriada
        self.races_label = tk.Label(self, text=f"Corridas cadastradas: {race_count}")
        self.races_label.pack()

        # Obtém a quantidade de temporadas (seasons) cadastradas
        season_count = self.get_season_count()  # Substitua com a função apropriada
        self.seasons_label = tk.Label(self, text=f"Temporadas cadastradas: {season_count}")
        self.seasons_label.pack()

        self.escuderia_button = tk.Button(self, text="Cadastrar Escuderias", command=lambda: self.master.switch_frame(EscuderiaRegisterFrame))
        self.escuderia_button.pack()

        self.piloto_button = tk.Button(self, text="Cadastrar Pilotos", command=lambda: self.master.switch_frame(PilotoRegisterFrame))
        self.piloto_button.pack()

        self.button = tk.Button(self, text="Ir para a Tela de relatórios", command=lambda: self.master.switch_frame(ThirdFrame))
        self.button.pack(pady=10)

    # Funções para obter as informações de overview
    def get_pilot_count(self):
        # Conecta ao banco de dados e obtém a quantidade de pilotos
        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM driver")
        pilot_count = c.fetchone()[0]
        conn.close()
        return pilot_count

    def get_constructor_count(self):
        # Inserir a query SQL para obter a quantidade de escuderias cadastradas
        pass

    def get_race_count(self):
        # Inserir a query SQL para obter a quantidade de corridas cadastradas
        pass

    def get_season_count(self):
        # Inserir a query SQL para obter a quantidade de temporadas cadastradas
        pass

# Define a janela para cadastro de escuderias
class EscuderiaRegisterFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.ref_label = tk.Label(self, text="Referência da Escuderia")
        self.ref_entry = tk.Entry(self)
        self.name_label = tk.Label(self, text="Nome da Escuderia")
        self.name_entry = tk.Entry(self)
        self.nationality_label = tk.Label(self, text="Nacionalidade")
        self.nationality_entry = tk.Entry(self)
        self.wiki_label = tk.Label(self, text="Link no Wikipédia")
        self.wiki_entry = tk.Entry(self)

        self.ref_label.pack()
        self.ref_entry.pack()
        self.name_label.pack()
        self.name_entry.pack()
        self.nationality_label.pack()
        self.nationality_entry.pack()
        self.wiki_label.pack()
        self.wiki_entry.pack()

        self.register_button = tk.Button(self, text="Cadastrar", command=self.register_escuderia)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(LoginSuccessFrame))
        self.back_button.pack()

    def register_escuderia(self):
        # Código para registrar a escuderia no banco de dados
        pass

# Define a janela para cadastro de pilotos
class PilotoRegisterFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.ref_label = tk.Label(self, text="Referência do Piloto")
        self.ref_entry = tk.Entry(self)
        self.number_label = tk.Label(self, text="Número de Corrida")
        self.number_entry = tk.Entry(self)
        self.code_label = tk.Label(self, text="Código (XXX)")
        self.code_entry = tk.Entry(self)
        self.name_label = tk.Label(self, text="Nome")
        self.name_entry = tk.Entry(self)
        self.surname_label = tk.Label(self, text="Sobrenome")
        self.surname_entry = tk.Entry(self)
        self.dob_label = tk.Label(self, text="Data de Nascimento (AAAA-MM-DD)")
        self.dob_entry = tk.Entry(self)
        self.nationality_label = tk.Label(self, text="Nacionalidade")
        self.nationality_entry = tk.Entry(self)

        self.ref_label.pack()
        self.ref_entry.pack()
        self.number_label.pack()
        self.number_entry.pack()
        self.code_label.pack()
        self.code_entry.pack()
        self.name_label.pack()
        self.name_entry.pack()
        self.surname_label.pack()
        self.surname_entry.pack()
        self.dob_label.pack()
        self.dob_entry.pack()
        self.nationality_label.pack()
        self.nationality_entry.pack()

        self.register_button = tk.Button(self, text="Cadastrar", command=self.register_piloto)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(LoginSuccessFrame))
        self.back_button.pack()

    def register_piloto(self):
        driverref = self.ref_entry.get()
        number = self.number_entry.get()
        code = self.code_entry.get()
        forename = self.name_entry.get()
        surname = self.surname_entry.get()
        dob = self.dob_entry.get()
        nationality = self.nationality_entry.get()

        driverid = 1000 + sum(ord(char) for char in driverref)

        db_config = get_config()
        conn = psycopg2.connect(**db_config)
        c = conn.cursor()

        try:
            c.execute("INSERT INTO driver (driverid, driverref, number, code, forename, surname, dob, nationality) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (driverid, driverref, number, code, forename, surname, dob, nationality))
            conn.commit()
            
            # Limpar os campos de entrada
            self.ref_entry.delete(0, tk.END)
            self.number_entry.delete(0, tk.END)
            self.code_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.surname_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.nationality_entry.delete(0, tk.END)

            messagebox.showinfo("Sucesso", "Piloto cadastrado com sucesso")
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            conn.close()

# Define a janela que exibe os dados buscados do banco de dados para Admin
class ThirdFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # código específico do Admin aqui
