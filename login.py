from customtkinter import *
from tkinter import messagebox

from painel import TelaPrincipal 
from usuario import Usuario, editar_historico, carregar_usuarios, registrar_usuario

from tela import BaseTela

import json

# login
#------
class TelaLogin(BaseTela):
    def __init__(self):
        super().__init__("Login", 350, 350)  # Configurações iniciais da tela
        global lista_usuarios
        lista_usuarios = carregar_usuarios()
        self.main()

    
    def main(self):

        # FRAME
        frame = CTkFrame(master=self, width=200, height=300, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        login_label = CTkLabel(master=frame, text="Bem-vindo!", font=("Roboto", 30))
        login_label.place(relx=0.5, y=70, anchor="center")

        # CAMPOS DE PREENCHIMENTO
        #------------------------
        usuario_entry = CTkEntry(master=frame, width=200, border_width=1, placeholder_text="Nome de usuario")
        usuario_entry.place(x=0, y=120)

        senha_entry = CTkEntry(master=frame, width=200, border_width=1, placeholder_text="Senha", show="*")
        senha_entry.place(x=0, y=160)

        # BOTOES
        #-------
        entrar_button = CTkButton(master=frame, text="Entrar", bg_color="transparent", fg_color="transparent",
                                 hover="disabled", text_color="gray", width=50,
                                 command=lambda: self.entrarConta(usuario_entry, senha_entry))
        entrar_button.place(x=0, y=190, anchor="nw")

        sem_conta_button = CTkButton(master=frame, text="Registrar", bg_color="transparent", fg_color="transparent", 
                                    hover="disabled", text_color="gray", width=80,
                                    command=lambda: self.telaRegistro())
        sem_conta_button.place(x=200, y=190, anchor="ne")

    def entrarConta(self, usuario_entry, senha_entry): 
        user = usuario_entry.get()
        senha = senha_entry.get()

        for u in lista_usuarios:
            if u.nome == user and u.senha == senha:
                self.destroy()
                app = TelaPrincipal(u)
                app.configure(fg_color="white")
                app.mainloop()
                return

        self.show_message("Erro", "Usuário ou senha inválido!", error=True)

    def telaRegistro(self):                            # indo para a tela de registro
        self.destroy()
        app = TelaRegistro()
        app.mainloop()


# registro
#---------
class TelaRegistro(BaseTela):
    def __init__(self):
        super().__init__("Registro", 350, 350)
        self.main()

    def main(self):
        # FRAME
        frame = CTkFrame(master=self, width=200, height=300, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        registro_label = CTkLabel(master=frame, text="Registrar", font=("Roboto", 30))
        registro_label.place(relx=0.5, y=70, anchor="center")

        # CAMPOS DE PREENCHIMENTO
        #------------------------
        usuario_entry = CTkEntry(master=frame, width=200, border_width=1, placeholder_text="Usuario")
        usuario_entry.place(x=0, y=120)

        senha_entry = CTkEntry(master=frame, width=200, border_width=1, placeholder_text="Senha", show="*")
        senha_entry.place(x=0, y=160)


        # BOTOES
        #-------
        voltar_button = CTkButton(master=frame, text="Voltar", bg_color="transparent", fg_color="transparent",
                                  hover="disabled", text_color="gray", width=40,
                                  command=lambda: self.telaLogin())
        voltar_button.place(x=0, y=190, anchor="nw")

        registrar_button = CTkButton(master=frame, text="Criar conta", bg_color="transparent", fg_color="transparent", 
                                    hover="disabled", text_color="gray", width=60,
                                    command=lambda: self.registrarConta(usuario_entry, senha_entry))
        registrar_button.place(x=200, y=190, anchor="ne")


    def registrarConta(self, usuario_entry, senha_entry):
        user = usuario_entry.get()
        senha = senha_entry.get()
        
        if not user or not senha:
            self.show_message("Erro", "Nome de usuário e senha não podem estar vazios!", error=True)
            return
        
        novo_usuario = Usuario(user, senha, None)
        if registrar_usuario(novo_usuario):
            self.show_message("Sucesso", "Conta criada com sucesso!")
            self.telaLogin()

            self.telaPrincipal()
        else:
            messagebox.showerror("Erro", "Erro ao criar conta!")

    def telaPrincipal(self):
        self.destroy()
        app = TelaPrincipal()
        app.configure(fg_color="#f4f4f4")
        app.mainloop()

    def telaLogin(self):
        self.destroy()
        app = TelaLogin()
        app.mainloop()
