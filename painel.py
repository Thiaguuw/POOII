from customtkinter import *
from PIL import Image, ImageTk
import requests
from tkinter import messagebox
from datetime import datetime, timedelta
from io import BytesIO
from historico import TelaHistorico
from pesquisa import Pesquisa

from tela import BaseTela

API_KEY = "d777e40f1aed4fcdbee225342240512"

class TelaPrincipal(BaseTela):
    def __init__(self, user):
        self.user = user
        super().__init__("Previsão do Tempo", 300, 350)
        self.main()

    def main(self):
        # frame do filtro
        frame = CTkFrame(master=self, width=300, height=100, fg_color="transparent")
        frame.pack(side="top", fill='x')

        # frame do tempo
        wframe = CTkScrollableFrame(master=self, width=300, height=250, fg_color="transparent")
        wframe.pack(side="top", fill='x')

        # Campo para selecionar a cidade
        city_entry = CTkEntry(master=frame, placeholder_text="Cidade", width=180, border_width=1.3,
                              corner_radius=10)
        city_entry.place(x=60, y=10)

        # Campo para a data de início
        start_date_label = CTkLabel(master=frame, text="Data de início:")
        start_date_label.place(x=10, y=40)
        start_date_entry = CTkEntry(master=frame, placeholder_text="AAAA-MM-DD", border_width=1.3,
                                    corner_radius=10)
        start_date_entry.place(x=10, y=60)

        # Campo para a data de fim
        end_date_label = CTkLabel(master=frame, text="Data de fim:", )
        end_date_label.place(x=150, y=40)
        end_date_entry = CTkEntry(master=frame, placeholder_text="AAAA-MM-DD", border_width=1.3,
                                  corner_radius=10)
        end_date_entry.place(x=150, y=60)

        # Botão para buscar previsão do tempo
        lupa_image = CTkImage(light_image=Image.open("assets/lupa.png"), size=(20, 20))
        search_button = CTkButton(master=frame, text="", image=lupa_image,
                                  border_width=1.2, bg_color="transparent", fg_color="whitesmoke", hover="disabled",
                                  text_color="#202020", corner_radius=10, width=10,
                                  command=lambda: self.fetch_weather(city_entry, start_date_entry, end_date_entry, wframe))
        search_button.place(x=290, y=10, anchor="ne")

        # Historico
        historico_image = CTkImage(light_image=Image.open("assets/historico.png"), size=(20,20))
        historico_button = CTkButton(master=frame, text="", image=historico_image,
                                     border_width=1.2, bg_color="transparent", fg_color="whitesmoke", hover="disabled",
                                     text_color="#202020", corner_radius=10, width=10,
                                     command=lambda: TelaHistorico(self, self.user))
        historico_button.place(x=10, y=10, anchor="nw")

    def calcular_dias(self, data_inicial, data_final):
        # Obter a data atual
        hoje = datetime.today()
        
        # Converter as strings para objetos de data
        try:
            data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d")
            data_final = datetime.strptime(data_final, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use o formato AAAA-MM-DD.")
            return False
        
        # Verificar se a data mínima é menor que a data de hoje
        if data_inicial.date() < hoje.date():
            messagebox.showerror("Erro", "A data mínima não pode ser menor que a data de hoje.")
            return False
        
        # Verificar se a data máxima está mais de 10 dias à frente
        if data_final > hoje + timedelta(days=10):
            messagebox.showerror("Erro", "A data máxima não pode ser mais de 10 dias à frente de hoje.")
            return False
        
        # Verificar se a data máxima é menor que a data mínima
        if data_final < data_inicial:
            messagebox.showerror("Erro", "A data máxima não pode ser anterior à data mínima.")
            return False
        
        # Calcular a diferença entre as datas
        diferença = data_final - data_inicial
        
        # Retornar o número de dias
        return abs(diferença.days)

    def fetch_weather(self, city_entry, start_entry, end_entry, wframe):
        # Implementar chamada para a API do OpenWeatherMap aqui
        city_entry = city_entry.get()
        start_entry = start_entry.get()
        end_entry = end_entry.get()

        dias_intervalo = self.calcular_dias(str(datetime.today().date()), str(start_entry))
        final_intervalo = self.calcular_dias(str(datetime.today().date()), str(end_entry))
        dias = self.calcular_dias(start_entry, end_entry)
        print(dias)
        if not str(dias).isdigit():
            return

        link = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_entry}&days={final_intervalo+1}&aqi=no&alerts=no&lang=pt"

        requisicao = requests.get(link)
        requisicao_json = requisicao.json()
        if str(requisicao) == "<Response [200]>":
            
            for widget in wframe.winfo_children():
                widget.destroy()

            city = city_entry
            country = requisicao_json["location"]["country"]
            
            city_label = CTkLabel(master=wframe, text=f"{city}, {country}", font=("Poplar Std", 22, "bold"),
                                  fg_color="#e7e7e7")
            city_label.place(relx=0.5, y=0, anchor="n")

            pesquisa = Pesquisa(city_entry, start_entry, end_entry)
            self.user.add_historico(pesquisa)
            for d in range(dias_intervalo, final_intervalo+1):
                dframe = CTkFrame(master=wframe, width=250, height=250, fg_color="#e7e7e7")
                dframe.pack(side="top", fill='x', pady=30)
                
                dia = requisicao_json["forecast"]["forecastday"][d]["date"]
                dia_label = CTkLabel(master=dframe, text=f"{dia}", font=("Poplar Std", 12, "bold"))
                dia_label.place(relx=0.5, y=0, anchor="n")
                # Frame roxo
                tempo_frame = CTkFrame(master=dframe, width=280, height=110, fg_color="#4d77bf", corner_radius=10)
                tempo_frame.place(relx=0.5, y=30, anchor="n")

                icone_url = "https:" + requisicao_json["forecast"]["forecastday"][d]["day"]["condition"]["icon"]
                response = requests.get(icone_url)
                img = Image.open(BytesIO(response.content))
                img = img.resize((64, 64))
                icone = CTkImage(light_image=img, size=(90, 90))

                icone_img = CTkLabel(master=tempo_frame, image=icone, text="")
                icone_img.place(x=20, rely=0.5, anchor="w")

                temp = requisicao_json["forecast"]["forecastday"][d]["day"]["avgtemp_c"]
                temp_label = CTkLabel(master=tempo_frame, text=f"{temp} C°", font=("Poplar Std", 34, "bold"), 
                                    text_color="#f4f4f4")
                temp_label.place(relx=0.4, rely=0.45, anchor="w")

                tempo = requisicao_json["forecast"]["forecastday"][d]["day"]["condition"]["text"]
                tempo_label = CTkLabel(master=tempo_frame, text=f"{tempo}", font=("Poplar Std", 12, "bold"), 
                                    text_color="#f4f4f4", height=10)
                tempo_label.place(relx=0.4, rely=0.7, anchor="w")

                # FRAMES INFO
                #------------

                # Temperatura Máxima
                temp_max = requisicao_json["forecast"]["forecastday"][d]["day"]["maxtemp_c"]

                temp_max_frame = CTkFrame(master=dframe, fg_color="transparent", width=125, height=40,
                                        corner_radius=10, border_width=1.3)
                temp_max_frame.place(x=10, y=150, anchor="nw")

                temp_max_image = CTkImage(light_image=Image.open("assets/max.png"), size=(20,20))
                temp_max_image_label = CTkLabel(master=temp_max_frame, text="", image=temp_max_image)
                temp_max_image_label.place(x=15, rely=0.5, anchor="w")

                temp_max_text_label = CTkLabel(master=temp_max_frame, text="Temp. max", font=("Poplar Std", 10, "bold"),
                                            height=10)
                temp_max_text_label.place(x=50, rely=0.25, anchor="w")
                temp_max_label = CTkLabel(master=temp_max_frame, text=f"{temp_max} C°", font=("Poplar Std", 12),
                                        height=10)
                temp_max_label.place(x=50, rely=0.6, anchor="w")


                # Temperatura Mínima
                temp_min = requisicao_json["forecast"]["forecastday"][d]["day"]["mintemp_c"]

                temp_min_frame = CTkFrame(master=dframe, fg_color="transparent", width=125, height=40,
                                        corner_radius=10, border_width=1.3)
                temp_min_frame.place(x=270, y=150, anchor="ne")

                temp_min_image = CTkImage(light_image=Image.open("assets/min.png"), size=(20,20))
                temp_min_image_label = CTkLabel(master=temp_min_frame, text="", image=temp_min_image)
                temp_min_image_label.place(x=15, rely=0.5, anchor="w")

                temp_min_text_label = CTkLabel(master=temp_min_frame, text="Temp. min", font=("Poplar Std", 10, "bold"),
                                            height=10)
                temp_min_text_label.place(x=50, rely=0.25, anchor="w")
                temp_min_label = CTkLabel(master=temp_min_frame, text=f"{temp_min} C°", font=("Poplar Std", 12),
                                        height=10)
                temp_min_label.place(x=50, rely=0.6, anchor="w")


                # Umidade
                umidade = requisicao_json["forecast"]["forecastday"][d]["day"]["avghumidity"]
                umidade_frame = CTkFrame(master=dframe, fg_color="transparent", width=125, height=40,
                                         corner_radius=10, border_width=1.3)
                umidade_frame.place(x=10, y=200, anchor="nw")

                umid_image = CTkImage(light_image=Image.open("assets/umidade.png"), size=(20,20))
                umid_image_label = CTkLabel(master=umidade_frame, text="", image=umid_image)
                umid_image_label.place(x=15, rely=0.5, anchor="w")

                umid_text_label = CTkLabel(master=umidade_frame, text="Umidade", font=("Poplar Std", 10, "bold"),
                                            height=10)
                umid_text_label.place(x=50, rely=0.25, anchor="w")
                umid_label = CTkLabel(master=umidade_frame, text=f"{umidade}%", font=("Poplar Std", 12),
                                        height=10)
                umid_label.place(x=50, rely=0.6, anchor="w")


                # Vento
                vento = requisicao_json["forecast"]["forecastday"][d]["day"]["maxwind_kph"]
                vento_frame = CTkFrame(master=dframe, fg_color="transparent", width=125, height=40,
                                         corner_radius=10, border_width=1.3)
                vento_frame.place(x=270, y=200, anchor="ne")

                vento_image = CTkImage(light_image=Image.open("assets/vento.png"), size=(20,20))
                vento_image_label = CTkLabel(master=vento_frame, text="", image=vento_image)
                vento_image_label.place(x=15, rely=0.5, anchor="w")

                vento_label = CTkLabel(master=vento_frame, text="Vento", font=("Poplar Std", 10, "bold"),
                                            height=10)
                vento_label.place(x=50, rely=0.25, anchor="w")
                vento_label = CTkLabel(master=vento_frame, text=f"{vento}km/h", font=("Poplar Std", 12),
                                        height=10)
                vento_label.place(x=50, rely=0.6, anchor="w")
