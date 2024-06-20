import os
from dbConnec import establecer_conexion, crear_tabla_dinamica_cme, insertar_datos_cme, verificar_tabla_existente_cme, crear_tabla_dinamica_asteroides, insertar_datos_asteroides, verificar_tabla_existente_asteroides
from apiData import obtener_datos_cme,obtener_datos_asteroides
from datosExcel import Verificacion_Excel_cme, insertar_datos_csv_cme,Verificacion_Excel_asteroides,insertar_datos_csv_asteroides
from analisisDatosApi import analizar_json_cme, analizar_json_asteroides

#API CME
def procesar_datos_api_cme():
    print("Starting data processing...")
    dataCme = obtener_datos_cme()
    if dataCme:
        values_list_cme = analizar_json_cme(dataCme)
        return values_list_cme
    return []

def crear_tabla_si_no_existe_cme():
    conn = establecer_conexion()
    if conn is not None:
        try:
            tabla = 'tabla_cme'
            if not verificar_tabla_existente_cme(conn, tabla):
                crear_tabla_dinamica_cme(conn, tabla)
        finally:
            conn.close()

def insertar_datos_en_db_cme(values_list_cme):
    conn = establecer_conexion()
    if conn is not None:
        try:
            crear_tabla_si_no_existe_cme()
            insertar_datos_cme(conn, 'tabla_cme', values_list_cme)
        finally:
            conn.close()

def verificar_y_crear_excel_cme():
    Verificacion_Excel_cme()

def insertar_datos_en_excel_cme(values_list_cme):
    if values_list_cme:
        nombre_archivo = os.path.join('src', 'CME.csv')
        insertar_datos_csv_cme(nombre_archivo, values_list_cme)


#API ASTEROIDES
def procesar_datos_api_asteroides():
    print("Starting data processing...")
    dataAsteroides = obtener_datos_asteroides()
    if dataAsteroides:
        values_list = analizar_json_asteroides(dataAsteroides)
        return values_list
    return []

def crear_tabla_si_no_existe_asteroides():
    conn = establecer_conexion()
    if conn is not None:
        try:
            tabla = 'tabla_asteroides'
            if not verificar_tabla_existente_asteroides(conn, tabla):
                crear_tabla_dinamica_asteroides(conn, tabla)
        finally:
            conn.close()

def insertar_datos_en_db_asteroides(values_list_asteroides):
    conn = establecer_conexion()
    if conn is not None:
        try:
            crear_tabla_si_no_existe_asteroides()
            insertar_datos_asteroides(conn, 'tabla_asteroides', values_list_asteroides)
        finally:
            conn.close()

def verificar_y_crear_excel_asteroides():
    Verificacion_Excel_asteroides()

def insertar_datos_en_excel_asteroides(values_list_asteroides):
    if values_list_asteroides:
        nombre_archivo = os.path.join('src', 'Asteroides.csv')
        insertar_datos_csv_asteroides(nombre_archivo, values_list_asteroides)


def main():
    values_list_cme = procesar_datos_api_cme()
    values_list_asteroides = procesar_datos_api_asteroides()

    if values_list_cme:
        insertar_datos_en_db_cme(values_list_cme)
        verificar_y_crear_excel_cme()
        insertar_datos_en_excel_cme(values_list_cme)

    if values_list_asteroides:
        insertar_datos_en_db_asteroides(values_list_asteroides)
        verificar_y_crear_excel_asteroides()
        insertar_datos_en_excel_asteroides(values_list_asteroides)