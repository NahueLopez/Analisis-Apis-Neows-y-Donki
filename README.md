# Proyecto de Análisis de la API de la NASA - NeoWs y DONKI

## URL base de la API de la NASA
`url base = 'https://api.nasa.gov/'`

## Descripción de las APIs

### NeoWs (Near Earth Object Web Service)
NeoWs es un servicio web RESTful para información de asteroides cercanos a la Tierra.

**Parámetros de consulta:**
- **fecha de inicio**: AAAA-MM-DD (ninguno por defecto) - Fecha de inicio de la búsqueda de asteroides.
- **fecha final**: AAAA-MM-DD (7 días después de la fecha_inicio por defecto) - Fecha de finalización de la búsqueda de asteroides.
- **Clave API**: cadena (DEMO_KEY por defecto) - Clave api.nasa.gov para uso ampliado.

### DONKI (Space Weather Database Of Notifications, Knowledge, Information)
DONKI proporciona datos sobre eventos climáticos espaciales, como eyecciones de masa coronal (CME).

**Parámetros de consulta:**
- **startDate**: AAAA-MM-DD - Fecha de inicio para la búsqueda de eventos CME.
- **endDate**: AAAA-MM-DD - Fecha de finalización para la búsqueda de eventos CME.
- **api_key**: cadena (DEMO_KEY por defecto) - Clave api.nasa.gov para uso ampliado.

## Descripción del Proyecto

El proyecto se plantea para recopilar los datos de las APIs NeoWs y DONKI, analizarlos y guardarlos en una base de datos y un archivo Excel. Se busca obtener solo los datos relevantes para el proyecto y evitar duplicados, utilizando la fecha de emisión y el ID de cada dato para verificar su unicidad.

Con las últimas modificaciones, el proyecto ahora cuenta con las siguientes mejoras:

- **Modularización del Main Script**: El script principal se ha dividido en múltiples tareas modulares, lo que permite una ejecución más clara y ordenada. Esto facilita la visualización del flujo de trabajo y permite optimizar cada paso por separado.
- **Docker**: Implementación de Docker y los archivos de configuración necesarios para asegurar un entorno de ejecución consistente y reproducible.
- **Airflow**: Implementación de Apache Airflow para la orquestación y automatización del flujo de trabajo.
- **DAGs en Airflow**: Se ha agregado el DAG necesario para el correcto funcionamiento del flujo de trabajo en Airflow, permitiendo la planificación y ejecución automática de las tareas.
- **Creación de Tareas en Airflow**: Se han creado tareas individuales en Airflow para cada parte del proceso, incluyendo la creación de tablas en la base de datos, el procesamiento de datos de la API, la verificación y creación de archivos Excel, y la inserción de datos en la base de datos y en el archivo Excel.
- **Optimización y Modularidad**: Continuas mejoras y modificaciones en el código para un mejor rendimiento y adaptabilidad a las necesidades del proyecto.
- **Mecanismo de Alerta**: Implementación de alertas por correo electrónico para valores que sobrepasen un límite específico.

## Funcionalidades del Proyecto

1. **Obtención de Datos**: Se accede a las APIs NeoWs y DONKI para obtener los datos necesarios.
2. **Conexión con Redshift**: Se establece una conexión con la base de datos Redshift.
3. **Análisis y Guardado de Datos**: Se analizan los datos JSON de las APIs y se guardan los campos relevantes.
4. **Verificación y Creación de Tabla**: Se verifica si la tabla de datos ya está creada; de lo contrario, se crea una nueva tabla.
5. **Almacenamiento de Datos**: Los datos procesados se insertan en la base de datos.
6. **Verificación y Creación del Excel**: Se verifica si el archivo Excel de datos ya está creado; de lo contrario, se crea un nuevo archivo Excel.
7. **Gestión de Errores**: Se implementa un manejo adecuado de errores y excepciones para garantizar que el programa pueda recuperarse de situaciones inesperadas y continuar su ejecución de manera segura.
8. **Modularización del Main Script**: Se modularizó el script principal para permitir la ejecución de múltiples tareas (tasks) de forma más clara y ordenada.
9. **Implementación de Docker**: Se añadió Docker para asegurar un entorno de ejecución consistente y reproducible, incluyendo los archivos de configuración necesarios.
10. **Implementación de Airflow**: Se integró Apache Airflow para la orquestación y automatización del flujo de trabajo.
11. **Creación de DAGs en Airflow**: Se agregó el DAG necesario para el correcto funcionamiento del flujo de trabajo en Airflow, permitiendo la planificación y ejecución automática de las tareas.
12. **Optimización y Modularidad**: Se continuó mejorando y modificando el código para un mejor rendimiento y adaptabilidad a las necesidades del proyecto.
13. **Mecanismo de Alerta**: Implementación de alertas por correo electrónico para valores que sobrepasen un límite específico.

## Pasa para Ejecutar el Proyecto:

1. **Clonar el Repositorio**: Clona el repositorio del proyecto desde GitHub en tu máquina local.
  git clone https://github.com/tu-usuario/nombre-del-repositorio.git
2. **Configurar Archivos Necesarios**: Asegúrate de tener los archivos apiKey.py y dbKey.py con las configuraciones necesarias en la raíz del proyecto.
3. **Abrir Docker Desktop**: Abre Docker Desktop en tu sistema operativo.
4. **Abrir Terminal**: Abre una terminal en la raíz del proyecto.
5. **Ejecutar Docker Compose**: Ejecuta el siguiente comando para construir y levantar los contenedores:
  docker-compose up
6. **Acceder al Proyecto**: Una vez que los contenedores estén en ejecución, puedes acceder al proyecto a través de tu navegador web en http://localhost:puerto, donde puerto es el puerto configurado en tu archivo   docker-compose.yml.

Con estos pasos, los usuarios podrán ejecutar tu proyecto de manera fácil y rápida.

## Consideraciones Importantes

### Archivos Faltantes

1. **Archivo apiKey.py**: Este archivo debe contener la variable `API_KEY`, que es la llave proporcionada por la API de la NASA.
2. **Archivo dbKey.py**: Este archivo debe contener las variables `DB_NAME`, `HOST`, `PORT`, `USER` y `PASSWORD`, que corresponden a los datos de la base de datos.
