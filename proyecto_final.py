# Pertenece a: Hernandez Camilo, Arocha Jezer, Gonzalez Juan, Estevez Alexandra, Vasquez Crisarys (Grupo 1IL131)

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import normaltest

# Cargar datos desde archivo CSV
csv_file = 'FPCPITOTLZGPAN.csv'
data_csv = pd.read_csv(csv_file)

# Convertir columnas a tipo adecuado
data_csv['DATE'] = pd.to_datetime(data_csv['DATE'])
data_csv['FPCPITOTLZGPAN'] = pd.to_numeric(data_csv['FPCPITOTLZGPAN'], errors='coerce')

# Reemplazar valores NaN por la media de la columna
data_csv['FPCPITOTLZGPAN'].fillna(data_csv['FPCPITOTLZGPAN'].mean(), inplace=True)

# Análisis descriptivo
print("Descripción de datos CSV:")
print(data_csv.describe())

# Prueba de normalidad
stat_csv, p_csv = normaltest(data_csv['FPCPITOTLZGPAN'].dropna())
print(f'Normalidad CSV: Statistics={stat_csv:.3f}, p={p_csv:.3f}')

# Filtrar datos por rango de años
def filtrar_por_anios(data, anio_inicio, anio_fin):
    return data[(data['DATE'].dt.year >= anio_inicio) & (data['DATE'].dt.year <= anio_fin)]

# Filtrar datos por rango de valores de inflación
def filtrar_por_inflacion(data, inflacion_min, inflacion_max):
    return data[(data['FPCPITOTLZGPAN'] >= inflacion_min) & (data['FPCPITOTLZGPAN'] <= inflacion_max)]

# Parámetros predefinidos
anio_inicio = 1980
anio_fin = 2000
inflacion_min = 0.5
inflacion_max = 10

# Filtrar datos
data_filtrada_anios = filtrar_por_anios(data_csv, anio_inicio, anio_fin)
data_filtrada_inflacion = filtrar_por_inflacion(data_csv, inflacion_min, inflacion_max)

# Funciones de visualización de gráficos
def mostrar_histograma():
    plt.figure(figsize=(10, 5))
    plt.hist(data_csv['FPCPITOTLZGPAN'], bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Histograma de la Inflación en Panamá')
    plt.xlabel('Inflación (%)')
    plt.ylabel('Frecuencia')
    plt.show()

def mostrar_dispersión():
    plt.figure(figsize=(10, 5))
    plt.scatter(data_csv['DATE'], data_csv['FPCPITOTLZGPAN'], alpha=0.7, color='blue')
    plt.title('Gráfico de Dispersión de la Inflación en Panamá')
    plt.xlabel('Fecha')
    plt.ylabel('Inflación (%)')
    plt.show()

def mostrar_caja():
    plt.figure(figsize=(10, 5))
    plt.boxplot(data_csv['FPCPITOTLZGPAN'])
    plt.title('Diagrama de Caja de la Inflación en Panamá')
    plt.ylabel('Inflación (%)')
    plt.show()

def mostrar_linea_tiempo():
    plt.figure(figsize=(10, 5))
    plt.plot(data_csv['DATE'], data_csv['FPCPITOTLZGPAN'], color='blue')
    plt.title('Línea de Tiempo de la Inflación en Panamá')
    plt.xlabel('Fecha')
    plt.ylabel('Inflación (%)')
    plt.show()

def mostrar_histograma_filtrado_anios():
    plt.figure(figsize=(10, 5))
    plt.hist(data_filtrada_anios['FPCPITOTLZGPAN'], bins=30, alpha=0.7, color='green', edgecolor='black')
    plt.title(f'Histograma de la Inflación en Panamá ({anio_inicio}-{anio_fin})')
    plt.xlabel('Inflación (%)')
    plt.ylabel('Frecuencia')
    plt.show()

def mostrar_histograma_filtrado_inflacion():
    plt.figure(figsize=(10, 5))
    plt.hist(data_filtrada_inflacion['FPCPITOTLZGPAN'], bins=30, alpha=0.7, color='red', edgecolor='black')
    plt.title(f'Histograma de la Inflación en Panamá ({inflacion_min}%-{inflacion_max}%)')
    plt.xlabel('Inflación (%)')
    plt.ylabel('Frecuencia')
    plt.show()

# Función de portada
def presentacion():
    portada = tk.Toplevel(root)
    portada.title("Presentación")
    portada.geometry("600x700")

    logo_utp = Image.open("logo_utp.png")
    logo_utp = logo_utp.resize((100, 100), Image.LANCZOS)
    logo_utp = ImageTk.PhotoImage(logo_utp)

    logo_fisc = Image.open("logo_fisc.png")
    logo_fisc = logo_fisc.resize((100, 100), Image.LANCZOS)
    logo_fisc = ImageTk.PhotoImage(logo_fisc)

    label_utp = tk.Label(portada, image=logo_utp)
    label_utp.place(x=20, y=20)

    label_fisc = tk.Label(portada, image=logo_fisc)
    label_fisc.place(x=480, y=20)

    info = ("UNIVERSIDAD TECNOLÓGICA DE PANAMÁ\n"
            "\nFACULTAD DE INGENIERÍA DE SISTEMAS COMPUTACIONALES\n"
            "\nLICENCIATURA EN INGENIERÍA DE SISTEMAS Y COMPUTACIÓN\n"
            "\nANALISIS DE DATOS Y TOMA DE DECISIONES\n"
            "\nPROYECTO FINAL\n"
            "\nHernandez, Camilo\n"
            "\nArocha, Jezer\n"
            "\nGonzalez, Juan\n"
            "\nEstevez, Alexandra\n"
            "\nVasquez, Crisarys\n"
            "\nGrupo: 1IL131\n"
            "\nSometido a criterio de: Javier Sanchezgalan.\n"
            "\nFecha: 22/7/2024")

    label_info = tk.Label(portada, text=info, justify="center", font=("Arial", 12))
    label_info.place(relx=0.5, rely=0.5, anchor="center")

    portada.mainloop()

# Controlador 1 (modificado): Mostrar inflación por década
def mostrar_inflacion_decada(decada):
    anio_inicio = decada
    anio_fin = decada + 9
    data_decada = filtrar_por_anios(data_csv, anio_inicio, anio_fin)
    if data_decada.empty:
        messagebox.showerror("Error", f"No hay datos disponibles para la década de {decada}s.")
        return

    ventana_decada = tk.Toplevel(root)
    ventana_decada.title(f'Inflación en la Década de {decada}s')
    ventana_decada.geometry("300x400")

    texto_inflacion = ""
    for index, row in data_decada.iterrows():
        texto_inflacion += f"Año {row['DATE'].year}: {row['FPCPITOTLZGPAN']:.2f}%\n"

    label_inflacion = tk.Label(ventana_decada, text=texto_inflacion, justify="left", font=("Arial", 10))
    label_inflacion.pack(pady=10)

def seleccionar_decada():
    ventana_decada = tk.Toplevel(root)
    ventana_decada.title("Seleccionar Década")
    ventana_decada.geometry("300x400")
    
    decadas = list(range(1960, 2030, 10))
    
    for decada in decadas:
        btn_decada = tk.Button(ventana_decada, text=f"Década de {decada}s", command=lambda d=decada: mostrar_inflacion_decada(d))
        btn_decada.pack(pady=5)

# Controlador 2: Mostrar gráfico de inflación por década
def mostrar_grafica_decada(decada):
    anio_inicio = decada
    anio_fin = decada + 9
    data_decada = filtrar_por_anios(data_csv, anio_inicio, anio_fin)
    if data_decada.empty:
        messagebox.showerror("Error", f"No hay datos disponibles para la década de {decada}s.")
        return
    plt.figure(figsize=(10, 5))
    plt.plot(data_decada['DATE'], data_decada['FPCPITOTLZGPAN'], label=f'Década de {decada}s')
    plt.title(f'Inflación en Panamá durante la Década de {decada}s')
    plt.xlabel('Fecha')
    plt.ylabel('Inflación (%)')
    plt.legend()
    plt.show()

def seleccionar_grafica_decada():
    ventana_decada = tk.Toplevel(root)
    ventana_decada.title("Seleccionar Década")
    ventana_decada.geometry("300x400")
    
    decadas = list(range(1960, 2030, 10))
    
    for decada in decadas:
        btn_decada = tk.Button(ventana_decada, text=f"Década de {decada}s", command=lambda d=decada: mostrar_grafica_decada(d))
        btn_decada.pack(pady=5)

# Función para salir de la aplicación
def salir():
    root.quit()

# Ventana principal
root = tk.Tk()
root.title("Dataset - Inflación en Panamá")
root.geometry("800x600")

# Imagen de fondo
imagen_fondo = Image.open("fondo.png")
imagen_fondo = imagen_fondo.resize((1200, 600), Image.LANCZOS)
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
fondo_label = tk.Label(root, image=imagen_fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Opciones principales
btn_presentacion = tk.Button(root, text="Presentación", command=presentacion, width=30)
btn_presentacion.pack(pady=10)

btn_histograma = tk.Button(root, text="Ver Histograma", command=mostrar_histograma, width=30)
btn_histograma.pack(pady=10)

btn_dispersión = tk.Button(root, text="Ver Gráfico de Dispersión", command=mostrar_dispersión, width=30)
btn_dispersión.pack(pady=10)

btn_caja = tk.Button(root, text="Ver Diagrama de Caja", command=mostrar_caja, width=30)
btn_caja.pack(pady=10)

btn_linea_tiempo = tk.Button(root, text="Ver Línea de Tiempo", command=mostrar_linea_tiempo, width=30)
btn_linea_tiempo.pack(pady=10)

btn_histograma_anios = tk.Button(root, text="Ver Histograma Filtrado por Años", command=mostrar_histograma_filtrado_anios, width=30)
btn_histograma_anios.pack(pady=10)

btn_histograma_inflacion = tk.Button(root, text="Ver Histograma Filtrado por Inflación", command=mostrar_histograma_filtrado_inflacion, width=30)
btn_histograma_inflacion.pack(pady=10)

btn_mostrar_inflacion = tk.Button(root, text="Mostrar Inflación por Década", command=seleccionar_decada, width=30)
btn_mostrar_inflacion.pack(pady=10)

btn_grafica_decada = tk.Button(root, text="Mostrar Gráfica por Década", command=seleccionar_grafica_decada, width=30)
btn_grafica_decada.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", command=salir, width=30)
btn_salir.pack(pady=10)

root.mainloop()
