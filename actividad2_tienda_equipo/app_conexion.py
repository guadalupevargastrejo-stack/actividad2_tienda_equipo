import streamlit as st
import psycopg2
from conexion import consultar

# 1. Título y nombre del equipo
st.title("Tienda de Abarrotes - Escenario 1")
st.caption(
    "Equipo: Zurisadai Cruz Valdez, Angel Aldahir Mejia Cabrera, Guadalupe Vargas Trejo, Hugo Rafael Castro Hernandez")

# 2. Sección de Datos de conexión
st.subheader("Datos de conexión")
col1, col2, col3, col4 = st.columns(4)
col1.write("**Servidor:** localhost")
col2.write("**Puerto:** 5432")
col3.write("**Base de datos:** tienda")
col4.write("**Usuario:** app_tienda")
st.write("**Contraseña:** ********")

# 3. Botón para probar conexión
if st.button("Probar conexión"):
    try:
        columnas, filas = consultar("SELECT current_database(), current_user, version();")
        resultado = filas[0]
        st.success(f"Conexión exitosa. Base: {resultado[0]}, Usuario: {resultado[1]}")
        st.info(f"Servidor: {resultado[2]}")
    except ValueError as e:
        st.error(str(e))
    except psycopg2.OperationalError:
        st.error(
            "Error operativo: No se pudo establecer conexión con PostgreSQL. Verifica que el servidor esté encendido y el puerto sea correcto.")
    except psycopg2.Error as e:
        st.error(f"Error de base de datos: {e.pgerror or e}")

# 4. Sección de Registros (Siempre visible)
st.subheader("Registros")

try:
    # Consulta unificada para métricas
    sql_metricas = "SELECT count(*), count(*) FILTER (WHERE activo) FROM productos;"
    _, filas_metricas = consultar(sql_metricas)
    total_registros = filas_metricas[0][0]
    total_activos = filas_metricas[0][1]

    # Mostrar métricas lado a lado
    met_col1, met_col2 = st.columns(2)
    met_col1.metric("Registros en la tabla", total_registros)
    met_col2.metric("Registros con estado activo", total_activos)

    # Filtro por categoría
    categorias = ["Todas", "Lácteos", "Bebidas", "Abarrotes", "Limpieza", "Botanas"]
    categoria_seleccionada = st.selectbox("Filtrar por categoría:", categorias)

    # Armado de consulta según filtro
    if categoria_seleccionada == "Todas":
        sql_tabla = "SELECT id_producto, codigo_producto, nombre_producto, categoria, precio, existencia, activo FROM productos ORDER BY id_producto;"
        parametros = ()
    else:
        sql_tabla = "SELECT id_producto, codigo_producto, nombre_producto, categoria, precio, existencia, activo FROM productos WHERE categoria = %s ORDER BY id_producto;"
        parametros = (categoria_seleccionada,)

    columnas_tabla, filas_tabla = consultar(sql_tabla, parametros)

    # Conversión del tipo Decimal a float para que Streamlit lo muestre bien
    filas_limpias = []
    for fila in filas_tabla:
        fila_lista = list(fila)
        fila_lista[4] = float(fila_lista[4])  # El índice 4 corresponde al precio
        filas_limpias.append(fila_lista)

    import pandas as pd

    df = pd.DataFrame(filas_limpias, columns=columnas_tabla)
    st.dataframe(df, hide_index=True, use_container_width=True)

except ValueError as e:
    st.error(str(e))
except psycopg2.OperationalError:
    st.error(
        "No se pudo conectar a la base de datos para cargar los registros. Revisa tus credenciales o el estado del servidor.")
except psycopg2.Error as e:
    st.error(f"Error al cargar los datos: {e.pgerror or e}")