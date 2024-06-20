import psycopg2
from psycopg2 import OperationalError
from dbKey import DB_NAME, HOST, PORT, USER, PASSWORD

def establecer_conexion():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD
        )
        print("Conectado a Redshift con éxito!")
        return conn

    except OperationalError as e:
        print(f'Error al establecer la conexión: {e}')
        return None

#API CME
def verificar_tabla_existente_cme(conn, table_name):
    try:
        with conn.cursor() as cur:
            # Verifica si la tabla ya existe en la base de datos
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
            exists = cur.fetchone()[0]
            return exists
    except Exception as e:
        print(f"Error al verificar la existencia de la tabla {table_name}: {e}")
        return False

def crear_tabla_dinamica_cme(conn, tabla):
    try:
        # Define las columnas de la tabla
        columnas = {
            'activityID': 'VARCHAR(512) PRIMARY KEY',
            'startTime': 'TIMESTAMP',
            'submissionTime': 'TIMESTAMP',
            'link': 'VARCHAR(512)',
            'fecha_creacion': 'DATE'
        }

        # Construir la definición de las columnas
        definicion_columnas = ", ".join([f"{nombre} {tipo}" for nombre, tipo in columnas.items()])

        with conn.cursor() as cur:
            # Crea la tabla si no existe
            cur.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({definicion_columnas});")
            conn.commit()
            print(f"Tabla '{tabla}' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

def insertar_datos_cme(conn, tabla, values_list_cme):
    activity_ids_existentes = set()
    datos_insertados = False
    try:
        with conn.cursor() as cur:
            print(f"DATOS A GUARDAR:{values_list_cme}")
            for evento in values_list_cme:

                # Modifica los nombres de las claves para que coincidan con los nombres de las columnas en la tabla
                activity_id = evento['activityID']
                start_time = evento['startTime']
                submission_time = evento['submissionTime']
                link = evento['link']
                fecha_creacion = evento['fecha_creacion']

                # Verifica si existen registros con el mismo activityID
                cur.execute(f"SELECT COUNT(*) FROM {tabla} WHERE activityid = %s", (activity_id,))
                if cur.fetchone()[0] == 0:
                    keys = list(evento.keys())
                    placeholders = ', '.join(['%s' for _ in range(len(keys))])
                    # Modifica los nombres de las columnas en la consulta INSERT INTO
                    query = f"INSERT INTO {tabla} (activityid, starttime, submissiontime, link, fecha_creacion) VALUES ({placeholders})"
                    values = [evento[key] for key in keys]
                    cur.execute(query, values)
                    datos_insertados = True
                else:
                    activity_ids_existentes.add(activity_id)
        conn.commit()
        if datos_insertados:
            print("Datos insertados correctamente.")
        if activity_ids_existentes:
            print(f"Los siguientes activityID ya existían en la tabla y no se agregaron nuevos registros para esos activityID: {', '.join(activity_ids_existentes)}")
        if not datos_insertados and not activity_ids_existentes:
            print("No se insertaron nuevos datos.")
    except Exception as e:
        print(f"Error al insertar datos en la tabla {tabla}: {e}")


#API ASTEROIDES
def verificar_tabla_existente_asteroides(conn, table_name):
    try:
        with conn.cursor() as cur:
            # Verifica si la tabla ya existe en la base de datos
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
            exists = cur.fetchone()[0]
            return exists
    except Exception as e:
        print(f"Error al verificar la existencia de la tabla {table_name}: {e}")
        return False

def crear_tabla_dinamica_asteroides(conn, tabla):
    try:
        # Define las columnas de la tabla
        columnas = {
            'id': 'VARCHAR(255) PRIMARY KEY',
            'fecha_creacion': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'fecha_emision': 'DATE',
            'name': 'VARCHAR(255)',
            'nasa_jpl_url': 'VARCHAR(255)',
            'absolute_magnitude_h': 'FLOAT',
            'relative_velocity': 'FLOAT',
            'miss_distance': 'FLOAT',
            'estimated_diameter_min_kilometers': 'FLOAT',
            'estimated_diameter_max_kilometers': 'FLOAT'
        }

        # Construir la definición de las columnas
        definicion_columnas = ", ".join([f"{nombre} {tipo}" for nombre, tipo in columnas.items()])

        with conn.cursor() as cur:
            # Crea la tabla si no existe
            cur.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({definicion_columnas});")
            conn.commit()
            print(f"Tabla '{tabla}' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

def insertar_datos_asteroides(conn, tabla, values_list_asteroides):
    fechas_existentes = set()
    datos_insertados = False
    try:
        with conn.cursor() as cur:
            for asteroid in values_list_asteroides:
                fecha_emision = asteroid['fecha_emision']
                id_asteroide = asteroid['id']
                # Verifica si existen registros con la misma fecha de emisión y ID
                cur.execute(f"SELECT COUNT(*) FROM {tabla} WHERE fecha_emision = %s AND id = %s", (fecha_emision, id_asteroide))
                if cur.fetchone()[0] == 0:
                    keys = list(asteroid.keys())
                    placeholders = ', '.join(['%s' for _ in range(len(keys))])
                    query = f"INSERT INTO {tabla} ({', '.join(keys)}) VALUES ({placeholders})"
                    values = [asteroid[key] for key in keys]
                    cur.execute(query, values)
                    datos_insertados = True
                else:
                    fechas_existentes.add(fecha_emision)
        conn.commit()
        if datos_insertados:
            print("Datos insertados correctamente.")
        if fechas_existentes:
            print(f"Las siguientes fechas de emisión ya tenían el ID registrado y no se agregaron nuevos registros para esos IDs: {', '.join(fechas_existentes)}")
        if not datos_insertados and not fechas_existentes:
            print("No se insertaron nuevos datos.")
    except Exception as e:
        print(f"Error al insertar datos en la tabla {tabla}: {e}")





