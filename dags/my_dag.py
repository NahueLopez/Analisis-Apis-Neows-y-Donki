from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.main import (
    crear_tabla_si_no_existe_cme,
    procesar_datos_api_cme,
    verificar_y_crear_excel_cme,
    insertar_datos_en_db_cme,
    insertar_datos_en_excel_cme,
    crear_tabla_si_no_existe_asteroides,
    procesar_datos_api_asteroides,
    verificar_y_crear_excel_asteroides,
    insertar_datos_en_db_asteroides,
    insertar_datos_en_excel_asteroides
)
from src.my_email import enviar_alerta_por_correo

default_args = {
    'owner': 'Nahuel',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mi_dag',
    default_args=default_args,
    description='Un DAG para ejecutar el script principal',
    schedule_interval=timedelta(days=1),
)

def start_system():
    print("Comienza el sistema...")

start_system_task = PythonOperator(
    task_id='start_system',
    python_callable=start_system,
    dag=dag,
)

# API CME
crear_tabla_cme_task = PythonOperator(
    task_id='crear_tabla_si_no_existe_cme',
    python_callable=crear_tabla_si_no_existe_cme,
    dag=dag,
)

def procesar_datos_api_y_guardar_cme(**kwargs):
    values_list_cme = procesar_datos_api_cme()
    kwargs['ti'].xcom_push(key='values_list_cme', value=values_list_cme)

procesar_datos_cme_task = PythonOperator(
    task_id='procesar_datos_api_y_guardar_cme',
    python_callable=procesar_datos_api_y_guardar_cme,
    provide_context=True,
    dag=dag,
)

def insertar_datos_en_db_cme_wrapper(**kwargs):
    values_list_cme = kwargs['ti'].xcom_pull(key='values_list_cme', task_ids='procesar_datos_api_y_guardar_cme')
    insertar_datos_en_db_cme(values_list_cme)

insertar_datos_db_cme_task = PythonOperator(
    task_id='insertar_datos_en_db_cme',
    python_callable=insertar_datos_en_db_cme_wrapper,
    provide_context=True,
    dag=dag,
)

def verificar_y_crear_excel_cme_wrapper(**kwargs):
    verificar_y_crear_excel_cme()

verificar_excel_cme_task = PythonOperator(
    task_id='verificar_y_crear_excel_cme',
    python_callable=verificar_y_crear_excel_cme_wrapper,
    dag=dag,
)

def insertar_datos_en_excel_cme_wrapper(**kwargs):
    values_list_cme = kwargs['ti'].xcom_pull(key='values_list_cme', task_ids='procesar_datos_api_y_guardar_cme')
    insertar_datos_en_excel_cme(values_list_cme)

insertar_datos_excel_cme_task = PythonOperator(
    task_id='insertar_datos_en_excel_cme',
    python_callable=insertar_datos_en_excel_cme_wrapper,
    provide_context=True,
    dag=dag,
)

def verificar_y_enviar_alertas_cme(**kwargs):
    values_list_cme = kwargs['ti'].xcom_pull(key='values_list_cme', task_ids='procesar_datos_api_y_guardar_cme')
    limite = 2  # Límite de Eyecciones de Masa Coronales en un día

    # Obtener la fecha actual
    now = datetime.now()
    fecha_actual = now.strftime("%Y-%m-%d")

    # Convertir la fecha actual a un objeto datetime para comparación
    fecha_actual_dt = datetime.strptime(fecha_actual, "%Y-%m-%d")

    # Filtrar las Eyecciones de Masa Coronales que ocurrieron en el día actual
    eyecciones_hoy = [cme for cme in values_list_cme if 'starttime' in cme and datetime.strptime(cme['starttime'], "%Y-%m-%d %H:%M:%S.%f").date() == fecha_actual_dt.date()]

    # Contar el número de Eyecciones de Masa Coronales en el día actual
    num_cme_hoy = len(eyecciones_hoy)

    # Mensaje de depuración
    print(f"Total de Eyecciones de Masa Coronales hoy: {num_cme_hoy}")
    print(f"Detalle de Eyecciones de Masa Coronales hoy: {eyecciones_hoy}")

    # Enviar alerta si se supera el límite
    if num_cme_hoy > limite:
        mensaje = f"Alerta: El número de Eyecciones de Masa Coronales supera el límite diario de {limite}. Total: {num_cme_hoy}\n{eyecciones_hoy}"
        enviar_alerta_por_correo(mensaje, "Alerta de Límite de Eyección de masa coronal", "nahu.cjs.nl@gmail.com", "nahu.cjs.nl@gmail.com", "smtp.gmail.com", 587, "nahu.cjs.nl@gmail.com", "seat quuc glrn eysk")
        print("Mensaje de alerta enviado.")
    elif num_cme_hoy > 0:
        mensaje = f"Aviso: Hubo {num_cme_hoy} Eyecciones de Masa Coronales hoy, todo dentro del límite.\n{eyecciones_hoy}"
        enviar_alerta_por_correo(mensaje, "Aviso de Eyección de masa coronal dentro del límite", "nahu.cjs.nl@gmail.com", "nahu.cjs.nl@gmail.com", "smtp.gmail.com", 587, "nahu.cjs.nl@gmail.com", "seat quuc glrn eysk")
        print("Mensaje de aviso enviado.")
    else:
        mensaje = f"Aviso: No hubo Eyecciones de Masa Coronales hoy."
        enviar_alerta_por_correo(mensaje, "Aviso de No Eyección de masa coronal", "nahu.cjs.nl@gmail.com", "nahu.cjs.nl@gmail.com", "smtp.gmail.com", 587, "nahu.cjs.nl@gmail.com", "seat quuc glrn eysk")
        print("Mensaje de no eyección enviado.")

    # Mensaje de verificación
    print("La función verificar_y_enviar_alertas_cme se ejecutó correctamente.")

verificar_alertas_cme_task = PythonOperator(
    task_id='verificar_y_enviar_alertas_cme',
    python_callable=verificar_y_enviar_alertas_cme,
    provide_context=True,
    dag=dag,
)

# API ASTEROIDES
crear_tabla_asteroides_task = PythonOperator(
    task_id='crear_tabla_si_no_existe_asteroides',
    python_callable=crear_tabla_si_no_existe_asteroides,
    dag=dag,
)

def procesar_datos_api_y_guardar_asteroides(**kwargs):
    values_list_asteroides = procesar_datos_api_asteroides()
    for asteroide in values_list_asteroides:
        asteroide['miss_distance'] = float(asteroide['miss_distance'])
    kwargs['ti'].xcom_push(key='values_list_asteroides', value=values_list_asteroides)

procesar_datos_asteroides_task = PythonOperator(
    task_id='procesar_datos_api_y_guardar_asteroides',
    python_callable=procesar_datos_api_y_guardar_asteroides,
    provide_context=True,
    dag=dag,
)

def insertar_datos_en_db_asteroides_wrapper(**kwargs):
    values_list_asteroides = kwargs['ti'].xcom_pull(key='values_list_asteroides', task_ids='procesar_datos_api_y_guardar_asteroides')
    insertar_datos_en_db_asteroides(values_list_asteroides)

insertar_datos_db_asteroides_task = PythonOperator(
    task_id='insertar_datos_en_db_asteroides',
    python_callable=insertar_datos_en_db_asteroides_wrapper,
    provide_context=True,
    dag=dag,
)

def verificar_y_crear_excel_asteroides_wrapper(**kwargs):
    verificar_y_crear_excel_asteroides()

verificar_excel_asteroides_task = PythonOperator(
    task_id='verificar_y_crear_excel_asteroides',
    python_callable=verificar_y_crear_excel_asteroides_wrapper,
    dag=dag,
)

def insertar_datos_en_excel_asteroides_wrapper(**kwargs):
    values_list_asteroides = kwargs['ti'].xcom_pull(key='values_list_asteroides', task_ids='procesar_datos_api_y_guardar_asteroides')
    insertar_datos_en_excel_asteroides(values_list_asteroides)

insertar_datos_excel_asteroides_task = PythonOperator(
    task_id='insertar_datos_en_excel_asteroides',
    python_callable=insertar_datos_en_excel_asteroides_wrapper,
    provide_context=True,
    dag=dag,
)

def verificar_y_enviar_alertas_asteroides(**kwargs):
    values_list_asteroides = kwargs['ti'].xcom_pull(key='values_list_asteroides', task_ids='procesar_datos_api_y_guardar_asteroides')
    limite = 24477.189490514  # Distancia mínima de acercamiento en km

    # Filtrar los asteroides que cumplen con la condición
    asteroides_cercanos = [asteroide for asteroide in values_list_asteroides if asteroide['miss_distance'] < limite]

    # Enviar alerta si hay asteroides cercanos
    if asteroides_cercanos:
        mensaje = f"Alerta: Se detectaron asteroides con una distancia de acercamiento menor a {limite} km.\n{asteroides_cercanos}"
        enviar_alerta_por_correo(mensaje, "Alerta de Asteroide Cercano", "nahu.cjs.nl@gmail.com", "nahu.cjs.nl@gmail.com", "smtp.gmail.com", 587, "nahu.cjs.nl@gmail.com", "seat quuc glrn eysk")
        print("Mensaje de alerta enviado.")
    else:
        mensaje = f"Aviso: No se detectaron asteroides con una distancia de acercamiento menor a {limite} km."
        enviar_alerta_por_correo(mensaje, "Aviso de No Asteroide Cercano", "nahu.cjs.nl@gmail.com", "nahu.cjs.nl@gmail.com", "smtp.gmail.com", 587, "nahu.cjs.nl@gmail.com", "seat quuc glrn eysk")
        print("Mensaje de no alerta enviado.")

    # Mensaje de verificación
    print("La función verificar_y_enviar_alertas_asteroides se ejecutó correctamente.")

verificar_alertas_asteroides_task = PythonOperator(
    task_id='verificar_y_enviar_alertas_asteroides',
    python_callable=verificar_y_enviar_alertas_asteroides,
    provide_context=True,
    dag=dag,
)

def end_system():
    print("Finalización del sistema...")

end_system_task = PythonOperator(
    task_id='end_system',
    python_callable=end_system,
    dag=dag,
)



# Definir la secuencia de tareas para CME
start_system_task >> procesar_datos_cme_task >> \
crear_tabla_cme_task >> insertar_datos_db_cme_task >> verificar_alertas_cme_task >> end_system_task
procesar_datos_cme_task >> verificar_excel_cme_task >> insertar_datos_excel_cme_task >> verificar_alertas_cme_task >> end_system_task

# Definir la secuencia de tareas para Asteroides
start_system_task >> procesar_datos_asteroides_task >> \
crear_tabla_asteroides_task >> insertar_datos_db_asteroides_task >> verificar_alertas_asteroides_task >> end_system_task
procesar_datos_asteroides_task >> verificar_excel_asteroides_task >> insertar_datos_excel_asteroides_task >> verificar_alertas_asteroides_task >> end_system_task