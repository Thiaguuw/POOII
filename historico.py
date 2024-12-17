from customtkinter import *
from tela import BaseTela

class TelaHistorico(BaseTela):
    def __init__(self, master, usuario):
        self.usuario = usuario
        super().__init__("Histórico", 350, 350)
        
        # Fazer a janela modal
        self.wait_visibility()
        self.grab_set()

        self.main()
    
    def main(self):
        frame = CTkFrame(master=self, fg_color="white")
        frame.pack(fill="both", expand=True)

        if not self.usuario.historico:
            CTkLabel(frame, text="Nenhum histórico encontrado").pack(pady=20)
        else:
            CTkLabel(frame, text="Histórico:").pack(pady=10)

            for h in self.usuario.historico:

                cidade_label = h.cidade
                start_date = h.start_date
                end_date = h.end_date

                text = f"Cidade: {cidade_label}\nDe: {start_date} Até: {end_date}\n"
                CTkLabel(frame, text=text, font=("Roboto", 12), anchor="w").pack(pady=5)
            pass
