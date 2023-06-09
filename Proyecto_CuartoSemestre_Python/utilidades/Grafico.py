import matplotlib.pyplot as plt

def grafico(datos):
    plt.figure(figsize=(8, 6))
    datos['d_estado'].value_counts().plot(kind='bar')
    plt.xlabel('Estado')
    plt.ylabel('Cantidad')
    plt.title('Distribución de códigos postales por estado')
    plt.xticks(rotation=70)
    plt.show()