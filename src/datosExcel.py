import os
import pandas as pd
from datetime import date

#API CME
def Verificacion_Excel_cme():
    nombre_archivo='CME.csv'
    # Obtener la ruta completa al archivo en la carpeta src
    ruta_archivo = os.path.join('src', nombre_archivo)

    if not os.path.isfile(ruta_archivo):
        # Definir las columnas
        columnas = [
            'activityID',
            'startTime',
            'submissionTime',
            'link',
            'fecha_creacion'
        ]
        # Crea un DataFrame con las columnas
        df = pd.DataFrame(columns=columnas)
        # Guardar el DataFrame en un archivo CSV con el delimitador
        df.to_csv(ruta_archivo, index=False, sep=';')
        print(f"Archivo '{ruta_archivo}' creado exitosamente con títulos de columnas.")
    else:
        print(f"El archivo '{ruta_archivo}' ya existe.")

def insertar_datos_csv_cme(nombre_archivo, values_list_cme):
    # Leer el archivo CSV existente
    df_existente = pd.read_csv(nombre_archivo, sep=';')

    # Agregar la fecha actual al campo 'fecha_creacion' para cada nuevo dato
    for row in values_list_cme:
        row['fecha_creacion'] = date.today().strftime('%Y-%m-%d')

    # Filtrar los datos que no están en el archivo existente
    nuevos_datos = [row for row in values_list_cme if row['startTime'] not in df_existente['startTime'].values]

    if nuevos_datos:
        # Convertir la lista de nuevas filas en un DataFrame
        nuevos_datos = pd.DataFrame(nuevos_datos, columns=df_existente.columns)
        # Concatenar el DataFrame existente con las nuevas filas
        df_actualizado = pd.concat([df_existente, nuevos_datos], ignore_index=True)
        # Guardar el DataFrame actualizado en el archivo CSV con el delimitador
        df_actualizado.to_csv(nombre_archivo, index=False, sep=';')
        print(f"Nuevos datos agregados al archivo '{nombre_archivo}'.")
    else:
        print("No hay datos nuevos que agregar.")


#API Asteroides
def Verificacion_Excel_asteroides():
    nombre_archivo='Asteroides.csv'
    # Obtener la ruta completa al archivo en la carpeta src
    ruta_archivo = os.path.join('src', nombre_archivo)

    if not os.path.isfile(ruta_archivo):
        # Definir las columnas
        columnas = [
            'id', 'fecha_creacion', 'fecha_emision', 'name',
            'nasa_jpl_url', 'absolute_magnitude_h',
            'relative_velocity', 'miss_distance',
            'estimated_diameter_min_kilometers', 'estimated_diameter_max_kilometers'
        ]
        # Crea un DataFrame con las columnas
        df = pd.DataFrame(columns=columnas)
        # Guardar el DataFrame en un archivo CSV con el delimitador
        df.to_csv(ruta_archivo, index=False, sep=';')
        print(f"Archivo '{ruta_archivo}' creado exitosamente con títulos de columnas.")
    else:
        print(f"El archivo '{ruta_archivo}' ya existe.")

def insertar_datos_csv_asteroides(nombre_archivo, values_list_asteroides):
    # Leer el archivo CSV existente
    df_existente = pd.read_csv(nombre_archivo, sep=';')

    # Verificar que la columna 'fecha_emision' existe en el DataFrame
    if 'fecha_emision' not in df_existente.columns:
        raise ValueError("La columna 'fecha_emision' no existe en el archivo CSV.")

    # Agregar la fecha actual al campo 'fecha_creacion' para cada nuevo dato
    for row in values_list_asteroides:
        row['fecha_creacion'] = date.today().strftime('%Y-%m-%d')

    # Filtrar los datos que no están en el archivo existente
    nuevos_datos = [row for row in values_list_asteroides if row['fecha_emision'] not in df_existente['fecha_emision'].values]

    if nuevos_datos:
        # Convertir la lista de nuevas filas en un DataFrame
        nuevos_datos = pd.DataFrame(nuevos_datos, columns=df_existente.columns)
        # Concatenar el DataFrame existente con las nuevas filas
        df_actualizado = pd.concat([df_existente, nuevos_datos], ignore_index=True)
        # Guardar el DataFrame actualizado en el archivo CSV con el delimitador
        df_actualizado.to_csv(nombre_archivo, index=False, sep=';')
        print(f"Nuevos datos agregados al archivo '{nombre_archivo}'.")
    else:
        print("No hay datos nuevos que agregar.")

