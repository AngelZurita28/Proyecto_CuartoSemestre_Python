import matplotlib.pyplot as plt
import dataclasses
import subprocess
import os
import tkinter as tk
from tkinter import *
from typing import List
import requests
import json

@dataclasses.dataclass
class Serie:
    titulo: str
    idSerie: str
    datos: List['DataSerie']

@dataclasses.dataclass
class DataSerie:
    fecha: str
    dato: str

@dataclasses.dataclass
class SeriesResponse:
    series: List[Serie]

@dataclasses.dataclass
class Response:
    bmx: SeriesResponse


def read_serie(baseURL):
    try:
        url = baseURL
        headers = {"Accept": "application/json", "Bmx-Token": "4adc3506701d0eb91bdef5e14a61fb67a560a59d2af45ec1655ffe52ec16aa5e"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Server error (HTTP {response.status_code}: {response.reason}).")
        
        json_response = json.loads(response.content)
        response.close()
        
        return json_response
    except Exception as e:
        print(e)

    return None

def api():
    ventana_api = tk.Tk()
    ventana_api.title("API BANXICO")
    ventana_api.geometry('400x150')
    
    lbFechaInicio = tk.Label(ventana_api, text="Fecha de inicio (AAAA-MM-DD)")
    lbFechaInicio.place(x=10, y=10)
    tbFechaInicio = tk.Entry(ventana_api, state='normal', width=28)
    tbFechaInicio.place(x=10, y=30)
    lbFechaFinal = tk.Label(ventana_api, text="Fecha de final (AAAA-MM-DD)")
    lbFechaFinal.place(x=200, y=10)
    tbFechaFinal = tk.Entry(ventana_api, state="normal",width=30)
    tbFechaFinal.place(x=200, y=30)

    boton_Fechas = Button(ventana_api, text="obtener valores",width=15, height=3)
    boton_Fechas.place(x=120, y=60)
    boton_Fechas.bind("<Button>", (lambda event: obtenerDeApi(tbFechaInicio.get(), tbFechaFinal.get())))

    ventana_api.mainloop()

def obtenerDeApi(inicio, final):
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos/{inicio}/{final}"
    print(url)
    response = read_serie(url)
    
    serie = response['bmx']['series'][0]
    datosY = []
    datosX = []

    with open("responseBanxico.txt", "w") as archivo:
        archivo.write(f"Serie: {serie['titulo']} \n")
        for data_serie in serie['datos']:
            if data_serie['dato'] == "N/E":
                continue
            archivo.write(f"Fecha: {data_serie['fecha']} \n")
            archivo.write(f"Dato: {data_serie['dato']} \n")
            datosY.append(float(data_serie['dato']))
            datosX.append(data_serie['fecha'])

    sp1 = subprocess.Popen(["notepad.exe", "responseBanxico.txt"])
    plt.figure(figsize=(8, 6))
    plt.plot(datosX, datosY)

    plt.show()
    sp1.wait()

    os.remove("responseBanxico.txt")