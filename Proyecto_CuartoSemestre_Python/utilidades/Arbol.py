import tkinter as tk
from tkinter import *
from tkinter import ttk

def arbol(datos):
    ventana = Tk()
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

            for codigo_postal in codigos_postales:
                nodo_codigo_postal = arbol.insert(nodo_ciudad, 'end', text=codigo_postal)
                calles = datos[(datos['d_estado'] == estado) & (datos['D_mnpio'] == ciudad) & (datos['d_codigo'] == codigo_postal)]['d_asenta']

                for calle in calles:
                    arbol.insert(nodo_codigo_postal, 'end', values=('', '', '', calle))

    arbol.pack(expand=True, fill=tk.BOTH)
    ventana.mainloop()
