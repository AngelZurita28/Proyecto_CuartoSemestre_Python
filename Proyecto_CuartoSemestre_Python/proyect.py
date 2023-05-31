import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from docx import Document
import json

# Función para leer el archivo CSV y devolver los datos como un DataFrame de Pandas
def leer_archivo_csv(ruta):
    with open(ruta, 'r') as archivo:
        lector_csv = csv.DictReader(archivo)
        datos = [fila for fila in lector_csv]
    return pd.DataFrame(datos)

def leer_archivo_texto(ruta):
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()

    datos = [linea.strip().split('|') for linea in lineas]
    encabezados = datos[0]
    datos = datos[1:]

    return pd.DataFrame(datos, columns=encabezados)


def mostrar_tabla(datos):
    ventana = tk.Tk()
    ventana.title("Tabla de datos")

    # Crear una tabla utilizando Treeview de ttk
    tabla = ttk.Treeview(ventana, selectmode='browse')
    tabla['columns'] = tuple(datos.columns)
    tabla['show'] = 'headings'

    # Configurar encabezados de columna
    for columna in datos.columns:
        tabla.heading(columna, text=columna)
        tabla.column(columna, width=100)

    # Agregar filas a la tabla
    for fila in datos.itertuples(index=False):
        tabla.insert('', 'end', values=tuple(fila))

    # Mostrar la tabla en la ventana
    tabla.pack(expand=True, fill=tk.BOTH)

    # Botón para guardar en csv
    # boton_guardarCSV = ttk.Button(ventana, text="CSV", command=guardarCSV(tabla))
    # boton_guardarCSV.pack()
    
    # # Boton para guardar en excel
    boton_guardarExcel = ttk.Button(ventana, text="Excel", Command=serializarTablaJson(datos))
    boton_guardarExcel.pack()

    # ventana.mainloop()

def serializarTablaJson(datos):
    # Convertir la tabla a un diccionario
    tabla_dict = {"columnas": list(datos.columns), "filas": datos.values.tolist()}

    # Serializar el diccionario a JSON
    tabla_json = json.dumps(tabla_dict, indent=4)

    # Guardar el JSON en un archivo
    with open("tabla.json", "w") as archivo:
        archivo.write(tabla_json)

def guardarWord(datos):
    # Crear un documento de Word
    doc = Document()

    # Crear una tabla en el documento
    tabla = doc.add_table(rows=1, cols=len(datos.columns))
    encabezados = tabla.rows[0].cells

    # Agregar encabezados de columna
    for i, columna in enumerate(datos.columns):
        encabezados[i].text = columna

    # Agregar filas con los datos de la tabla
    for fila in datos.itertuples(index=False):
        nueva_fila = tabla.add_row().cells
        for i, valor in enumerate(fila):
            nueva_fila[i].text = str(valor)

    # Guardar el documento en un archivo
    doc.save("tabla.docx")

def guardarCSV(tabla):
    # Actualizar los datos en el DataFrame de Pandas
    messagebox.showinfo("buenas")
    for fila in tabla.get_children():
        valores = tabla.item(fila)['values']
        indice = tabla.index(fila)
        for col, val in enumerate(valores):
            datos.iat[indice, col] = val
    # Guardar el DataFrame actualizado en un archivo
    datos.to_csv('datos_actualizados.csv', index=False)

def guardarExcel(datos):
    archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                           filetypes=[("Archivo de Excel", "*.xlsx"), ("Todos los archivos", "*.*")])
    if archivo:
        print(f"Archivo seleccionado: {archivo}")
    datos.to_excel(archivo, index=False)

# Función para mostrar los datos en un gráfico utilizando matplotlib
def mostrar_grafico(datos):
    plt.figure(figsize=(8, 6))
    datos['d_estado'].value_counts().plot(kind='bar')
    plt.xlabel('Estado')
    plt.ylabel('Cantidad')
    plt.title('Distribución de códigos postales por estado')
    plt.xticks(rotation=45)
    plt.show()


# Función para mostrar los datos en una vista de árbol desplegable utilizando tkinter
def mostrar_arbol(datos):
    ventana = tk.Tk()
    ventana.title("Vista de Árbol")

    arbol = ttk.Treeview(ventana)
    arbol['columns'] = ('Colonia', 'Ciudad', 'Código Postal', 'Calles')

    arbol.column('#0', width=100, minwidth=100)
    arbol.column('Colonia', width=100, minwidth=100)
    arbol.column('Ciudad', width=100, minwidth=100)
    arbol.column('Código Postal', width=100, minwidth=100)
    arbol.column('Calles', width=100, minwidth=100)

    arbol.heading('#0', text='Estado', anchor=tk.W)
    arbol.heading('Colonia', text='Colonia', anchor=tk.W)
    arbol.heading('Ciudad', text='Ciudad', anchor=tk.W)
    arbol.heading('Código Postal', text='Código Postal', anchor=tk.W)
    arbol.heading('Calles', text='Calles', anchor=tk.W)

    estados = set(datos['d_estado'])

    for estado in estados:
        nodo_estado = arbol.insert('', 'end', text=estado)
        ciudades = set(datos[datos['d_estado'] == estado]['D_mnpio'])

        for ciudad in ciudades:
            nodo_ciudad = arbol.insert(nodo_estado, 'end', text=ciudad)
            codigos_postales = datos[(datos['d_estado'] == estado) & (datos['D_mnpio'] == ciudad)]['d_codigo']
            print(type(codigos_postales))

            for codigo_postal in codigos_postales:
                # if codigo_postal in arbol.get_children:
                #     continue
                nodo_codigo_postal = arbol.insert(nodo_ciudad, 'end', text=codigo_postal)
                calles = datos[(datos['d_estado'] == estado) & (datos['D_mnpio'] == ciudad) & (datos['d_codigo'] == codigo_postal)]['d_asenta']

                for calle in calles:
                    arbol.insert(nodo_codigo_postal, 'end', values=('', '', '', calle))

    arbol.pack(expand=True, fill=tk.BOTH)
    ventana.mainloop()

if __name__ == '__main__':
    mainWindow = tk.Tk()
    mainWindow.title("Main")
    mainWindow.geometry("300x300")

    ruta_archivo = 'datos.txt'
    datos = leer_archivo_texto(ruta_archivo)


    boton_Tabla = tk.Button(mainWindow, text="Tabla", height=3, width=10, command=mostrar_tabla(datos))
    boton_Tabla.pack(padx=10, pady=10)
    boton_Grafica = tk.Button(mainWindow, height=3, width=10, text="Grafica")
    boton_Grafica.pack(padx=10, pady=10)
    boton_Arbol = tk.Button(mainWindow, height=3, width=10, text="Arbol")
    boton_Arbol.pack(padx=10, pady=10)

    mainWindow.mainloop()
