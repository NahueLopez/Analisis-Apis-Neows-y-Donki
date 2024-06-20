import datetime

def analizar_json_cme(data):
    # Analizo el JSON de datos de CME de la API y guardo los valores relevantes para cada evento
    all_values = []
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')  # Fecha actual en formato YYYY-MM-DD

    for event in data:
        values = {
            'activityID': event.get('activityID', None),
            'startTime': event.get('startTime', None),
            'submissionTime': event.get('submissionTime', None),
            'link': event.get('link', None),
            'fecha_creacion': today  # Agregar la fecha del día
        }
        all_values.append(values)
    print(f"Datos Analizados: {all_values}")
    return all_values

def analizar_json_asteroides(data):
    # Analizo el JSON de datos de asteroides de la api y guardo los valores relevantes para cada asteroide
    all_values = []
    near_earth_objects = data.get('near_earth_objects', {})

    for fecha, asteroids in near_earth_objects.items():
        for asteroid in asteroids:
            close_approach_data = asteroid.get('close_approach_data', [])
            if close_approach_data:
                values = {
                    'id': asteroid.get('neo_reference_id', None),
                    'name': asteroid.get('name', None),
                    'nasa_jpl_url': asteroid.get('nasa_jpl_url', None),
                    'absolute_magnitude_h': asteroid.get('absolute_magnitude_h', None),
                    'relative_velocity': close_approach_data[0]['relative_velocity'].get('kilometers_per_hour', None),
                    'miss_distance': close_approach_data[0]['miss_distance'].get('kilometers', None),
                    'estimated_diameter_min_kilometers': asteroid['estimated_diameter']['kilometers'].get(
                        'estimated_diameter_min', None),
                    'estimated_diameter_max_kilometers': asteroid['estimated_diameter']['kilometers'].get(
                        'estimated_diameter_max', None),
                    'fecha_emision': fecha
                }
                all_values.append(values)
    return all_values
