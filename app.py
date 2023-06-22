import psycopg2  # Importa o módulo psycopg2 para conectar com o PostgreSQL
import tkinter as tk  # Importa o módulo tkinter para criar a GUI
from tkinter import messagebox  # Importa messagebox para exibir caixas de mensagem
import configparser  # Importa configparser para ler o arquivo config.ini
from admin import LoginSuccessFrame as AdminLoginSuccessFrame, ThirdFrame as AdminThirdFrame
from escuderia import LoginSuccessFrame as EscuderiaLoginSuccessFrame, ThirdFrame as EscuderiaThirdFrame
from piloto import LoginSuccessFrame as PilotoLoginSuccessFrame, ThirdFrame as PilotoThirdFrame

# Conexão com o banco de dados
def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['postgresql']

# Função para logar o usuário
def login(username, password):
    db_config = get_config()
    conn = psycopg2.connect(**db_config)
    c = conn.cursor()

    # Confere se o usuário existe na base de dados e a senha está correta
    c.execute("SELECT userid, tipo FROM users WHERE login=%s AND password=md5(%s)", (username, password))
    result = c.fetchone()

    if result is not None:
        user_id, user_type = result
        
        # Insere um registro na tabela Log_Table
        c.execute("INSERT INTO log_table (UserId, LoginDate, LoginTime) VALUES (%s, CURRENT_DATE, CURRENT_TIME)", (user_id,))
        conn.commit()
        conn.close()

        return user_type  # retornando o tipo de usuário
    else:
        conn.close()
        return None

# Define a janela de login
class LoginFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Cria os widgets para entrada do nome de usuário e senha e o botão para logar
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
        user_type = login(username, password)
        if user_type:
            self.master.current_user = username  # armazenando o usuário atual

            if user_type == 'Administrador':
                frame_class = AdminLoginSuccessFrame
            elif user_type == 'Escuderia':
                frame_class = EscuderiaLoginSuccessFrame
            elif user_type == 'Piloto':
                frame_class = PilotoLoginSuccessFrame
            else:
                raise ValueError(f"User type {user_type} not recognized")

            self.master.switch_frame(frame_class, username)
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos!")

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

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
