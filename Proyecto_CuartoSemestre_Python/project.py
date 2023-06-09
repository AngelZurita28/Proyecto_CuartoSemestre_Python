from utilidades.Grafico import *
from utilidades.Tabla import *
from utilidades.Arbol import *
from utilidades.Api import *
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog

def leer_archivo_texto(ruta):
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
    datos = [linea.strip().split('|') for linea in lineas]
    encabezados = datos[0]
    datos = datos[1:]
    return pd.DataFrame(datos, columns=encabezados)
    
if __name__ == '__main__':
    mainWindow = Tk()
    mainWindow.title("Main")
    mainWindow.geometry("250x150")

    ruta_archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")])
    datos = leer_archivo_texto(ruta_archivo)
    boton_Tabla = Button(mainWindow,width=13, height=3, text="Tabla")
    boton_Tabla.bind("<Button>", (lambda event: tabla(datos)))
    boton_Tabla.place(x=20, y=20)

    boton_Grafica = tk.Button(mainWindow,width=13, height=3, text="Grafica")
    boton_Grafica.bind("<Button>", (lambda event: grafico(datos)))
    boton_Grafica.place(x=130, y=20)

    boton_Arbol = tk.Button(mainWindow,width=13, height=3, text="Arbol")
    boton_Arbol.bind("<Button>", (lambda event: arbol(datos)))
    boton_Arbol.place(x=20, y=80)
    
    boton_Api = Button(mainWindow, width=13, height=3, text='API')
    boton_Api.bind("<Button>", (lambda event: api()))
    boton_Api.place(x=130, y=80)

    mainWindow.mainloop()