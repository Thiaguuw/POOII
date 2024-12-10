from customtkinter import *

class TelaHistorico(CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master=master)
        self.usuario = usuario

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = 350
        height = 350

        self.title("Histórico")
        self.geometry(f"{width}x{height}+{screen_width//2-width//2}+{screen_height//2-height//2}")
        self.resizable(False, False)
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