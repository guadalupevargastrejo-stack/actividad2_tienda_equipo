import os
import psycopg2
from dotenv import load_dotenv

# Cargamos las variables del archivo .env al entorno
load_dotenv()


def obtener_conexion():
    """Establece y devuelve la conexión a PostgreSQL validando variables de entorno."""

    # Definimos las variables obligatorias que nuestro programa necesita
    variables_requeridas = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
    faltantes = []

    # Revisamos una por una si existen en el entorno
    for var in variables_requeridas:
        if not os.getenv(var):
            faltantes.append(var)

    # Si falta alguna variable, detenemos el proceso con un mensaje claro
    if faltantes:
        raise ValueError(f"Faltan variables en el archivo .env: {', '.join(faltantes)}")

    # Asignamos valores por defecto seguros para host y puerto si no existen
    host = os.getenv('DB_HOST') or 'localhost'
    puerto = int(os.getenv('DB_PORT') or '5432')

    # Intentamos establecer la conexión con un tiempo límite de 5 segundos
    conexion = psycopg2.connect(
        host=host,
        port=puerto,
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        connect_timeout=5
    )

    return conexion


def consultar(sql, parametros=()):
    """Ejecuta una consulta SQL y devuelve los nombres de las columnas y las filas."""
    conexion = None
    try:
        # Abrimos la conexión y preparamos el cursor
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Ejecutamos la consulta protegiéndonos con parámetros (%s)
        cursor.execute(sql, parametros)

        # Extraemos los nombres de las columnas del objeto description
        columnas = [d[0] for d in cursor.description]

        # Recuperamos todas las filas resultantes
        filas = cursor.fetchall()
        return columnas, filas

    finally:
        # Este bloque se ejecuta siempre, haya error o no, garantizando liberar recursos
        if conexion is not None:
            cursor.close()
            conexion.close()