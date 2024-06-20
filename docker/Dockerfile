# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copiar el archivo requirements.txt al contenedor
COPY docker/requirements.txt ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del directorio src al directorio de trabajo en el contenedor
COPY src/ .

# Copiar el archivo del DAG al directorio de dags en el contenedor de Airflow
COPY dags/ /usr/local/airflow/dags/

# Configurar Airflow
ENV AIRFLOW_HOME=/usr/local/airflow
RUN airflow db init

# Comando para iniciar el scheduler y el webserver de Airflow
CMD ["sh", "-c", "airflow scheduler & airflow webserver -p 8080"]
