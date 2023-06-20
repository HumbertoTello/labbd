import psycopg2  # Importa o módulo psycopg2 para conectar com o PostgreSQL
import tkinter as tk  # Importa o módulo tkinter para criar a GUI
from tkinter import messagebox, ttk  # Importa messagebox para exibir caixas de mensagem e ttk para widgets temáticos
import configparser # Importa o configparser para ler o arquivo config.ini

# Conexão com o banco de dados
def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['postgresql']

config = get_config()
conn = psycopg2.connect(database=config['database'], user=config['user'], password=config['password'], host=config['host'], port=config['port'])

# Define a janela de login
class LoginFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Cria os widgets para entrada do nome de usuário e senha, e os botões para logar
        self.username_label = tk.Label(self, text="Nome de usuário")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Senha")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login_user)
        self.login_button.pack()

    # Função para logar o usuário
    def login_user(self):
        # Pega o nome de usuário e a senha inseridos
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Erro", "Ambos os campos são obrigatórios!")
            return

        # Confere se o usuário existe na base de dados e a senha está correta
        is_authenticated = login(username, password)
        if is_authenticated:
            self.master.current_user = username  # armazenando o usuário atual
            self.master.switch_frame(LoginSuccessFrame, username)
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos!")

# Define a janela exibida após o login bem-sucedido
class LoginSuccessFrame(tk.Frame):
    def __init__(self, master=None, username=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=f"Olá, {username}!")
        self.label.pack()

        self.button = tk.Button(self, text="Ir para a Tela 3", command=lambda: self.master.switch_frame(ThirdFrame))
        self.button.pack()

# Função para buscar dados do banco de dados
def fetch_data():
    # Conecta com o banco de dados
    db_config = get_config()
    conn = psycopg2.connect(**db_config)
    c = conn.cursor()

    # Busca os dados
    c.execute("SELECT name, year FROM races LIMIT 10")
    rows = c.fetchall()
    
    # Fecha a conexão e retorna os dados
    conn.close()

    return rows

# Define a janela que exibe os dados buscados do banco de dados
class ThirdFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text="Bem-vindo à Tela 3!")
        self.label.pack()

        self.tree = ttk.Treeview(self, columns=('Name', 'Year'), show='headings')
        self.tree.heading('Name', text='Nome')
        self.tree.heading('Year', text='Ano')
        self.tree.pack()

        data = fetch_data()
        for row in data:
            self.tree.insert('', 'end', values=row)

        self.button = tk.Button(self, text="Voltar", command=lambda: self.master.switch_frame(LoginSuccessFrame, self.master.current_user))  # usando o usuário atual
        self.button.pack()

# Define a janela de login do aplicativo
class MainApp(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("640x480")  # Definindo o tamanho da janela
        self.title("Fórmula 1")
        self.current_user = None  # adicionando um atributo para armazenar o usuário atual
        self.switch_frame(LoginFrame)

    # Função para alternar entre janelas
    def switch_frame(self, frame_class, *args, **kwargs):
        current_frame = frame_class(self, *args, **kwargs)
        current_frame.pack()
        
        for frame in self.pack_slaves():
            if frame is not current_frame:
                frame.pack_forget()

# Função para registrar o usuário
def register(username, password):
    db_config = get_config()
    conn = psycopg2.connect(**db_config)
    c = conn.cursor()

    # Insere o novo usuário na base de dados
    c.execute("INSERT INTO users (login, password) VALUES (%s, md5(%s))", (username, password))
    
    conn.commit()
    conn.close()

# Função para logar o usuário
def login(username, password):
    db_config = get_config()
    conn = psycopg2.connect(**db_config)
    c = conn.cursor()

    # Confere se o usuário existe na base de dados e a senha está correta
    c.execute("SELECT * FROM users WHERE login=%s AND password=md5(%s)", (username, password))
    user = c.fetchone()
    
    conn.close()

    return user is not None

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
