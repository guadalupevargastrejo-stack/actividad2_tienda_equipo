# Actividad 2: Conexión a una base de datos PostgreSQL (Tienda de abarrotes)
**Equipo:** Zurisadai Cruz Valdez, Angel Aldahir Mejia Cabrera, Guadalupe Vargas Trejo, Hugo Rafael Castro Hernandez

Creación de una base de datos relacional robusta en PostgreSQL y desarrollo de una aplicación web en Streamlit para visualizar datos mediante conexiones seguras (DB-API) usando variables de entorno.

### Requisitos
- Python 3.10+
- PostgreSQL 15 o superior

### Instrucciones de uso
1. **Base de datos:** Abre pgAdmin, conéctate al servidor predeterminado y ejecuta el script `crear_bd.sql`.
2. **Instalación:** Ejecuta en la terminal `pip install -r requirements.txt`.
3. **Configuración:** Copia el archivo `.env.example`, renómbralo a `.env` y coloca tu contraseña de PostgreSQL.
4. **Ejecución:** Ejecuta `streamlit run app_conexion.py` y abre la URL local en tu navegador.