from customtkinter import *
from tkinter import messagebox

class BaseTela(CTk):
    def __init__(self, title, width, height):
        super().__init__()

        self.title(title)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Centralizar a janela
        self.geometry(f"{width}x{height}+{screen_width//2-width//2}+{screen_height//2-height//2}")
        self.resizable(False, False)

    def show_message(self, title, message, error=False):
        if error:
            from tkinter import messagebox
            messagebox.showerror(title, message)
        else:
            from tkinter import messagebox
            messagebox.showinfo(title, message)
