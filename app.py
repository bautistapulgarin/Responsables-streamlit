# streamlit run app.py

import streamlit as st
import pandas as pd
import base64
import io

# ----------------------------
# Configuración general
# ----------------------------
st.set_page_config(page_title="Seguimiento de Proyectos", layout="wide")

# ----------------------------
# Función para cargar Excel desde GitHub (carpeta /data)
# ----------------------------
@st.cache_data
def cargar_excel(nombre_archivo):
    try:
        df = pd.read_excel(f"data/{nombre_archivo}")
        df.columns = df.columns.str.strip().str.upper()
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()

# ----------------------------
# Función para generar descarga en Excel
# ----------------------------
def descargar_excel(df, nombre="descarga.xlsx"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    datos = output.getvalue()
    b64 = base64.b64encode(datos).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre}">📥 Descargar Excel</a>'
    return href

# ----------------------------
# Interfaz principal
# ----------------------------
st.title("📊 Panel de Seguimiento de Proyectos")

tabs = st.tabs(["Consulta de Responsables", "Reporte de Avances", "Horario de Reuniones"])

# ===============================================================
# 🟦 Pestaña 1: Consulta de Responsables
# ===============================================================
with tabs[0]:
    st.subheader("🔍 Consulta de Responsables")

    df_resp = cargar_excel("Responsables.xlsx")

    if not df_resp.empty:
        col1, col2, col3, col4 = st.columns(4)
        sucursal = col1.selectbox("Sucursal", ["Todos"] + sorted(df_resp["Sucursal"].dropna().unique().tolist()))
        cluster = col2.selectbox("Cluster", ["Todos"] + sorted(df_resp["Cluster"].dropna().unique().tolist()))
        proyecto = col3.selectbox("Proyecto", ["Todos"] + sorted(df_resp["Proyecto"].dropna().unique().tolist()))
        cargo = col4.selectbox("Cargo", ["Todos"] + sorted(df_resp["Cargo"].dropna().unique().tolist()))

        col5, col6, col7 = st.columns(3)
        estado = col5.selectbox("Estado", ["Todos"] + sorted(df_resp["Estado"].dropna().unique().tolist()))
        gerente = col6.selectbox("Gerente de Proyecto", ["Todos"] + sorted(df_resp["Gerente"].dropna().unique().tolist()))
        busqueda = col7.text_input("Búsqueda por texto (nombre o correo):")

        df_filtrado = df_resp.copy()

        if sucursal != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Sucursal"] == sucursal]
        if cluster != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Cluster"] == cluster]
        if proyecto != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Proyecto"] == proyecto]
        if cargo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Cargo"] == cargo]
        if estado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Estado"] == estado]
        if gerente != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Gerente"] == gerente]
        if busqueda:
            df_filtrado = df_filtrado[df_filtrado.apply(lambda r: busqueda.lower() in str(r.values).lower(), axis=1)]

        st.dataframe(df_filtrado, use_container_width=True)
        st.markdown(descargar_excel(df_filtrado, "Responsables_filtrados.xlsx"), unsafe_allow_html=True)

    else:
        st.warning("No se pudo cargar la información de responsables.")

# ===============================================================
# 🟩 Pestaña 2: Reporte de Avances
# ===============================================================
with tabs[1]:
    st.subheader("📈 Reporte de Avances")

    df_avances = cargar_excel("ReporteAvances.xlsx")

    if not df_avances.empty:
        st.dataframe(df_avances, use_container_width=True)
        st.markdown(descargar_excel(df_avances, "ReporteAvances.xlsx"), unsafe_allow_html=True)
    else:
        st.warning("No se pudo cargar la información del reporte de avances.")

# ===============================================================
# 🟨 Pestaña 3: Horario de Reuniones
# ===============================================================
with tabs[2]:
    st.subheader("🕒 Horario de Reuniones - Last Planner System")

    df_horarios = cargar_excel("HorariosReuniones.xlsx")

    if not df_horarios.empty:
        columnas_requeridas = [
            "SUCURSAL", "PRACTICANTE", "GERENTE", "PROYECTO",
            "DIA INTERMEDIA", "HORA INTERMEDIA", "DIA SEMANAL", "HORA SEMANAL"
        ]

        # Verificar que el archivo tiene las columnas esperadas
        columnas_archivo = [c.upper() for c in df_horarios.columns]
        if not all(col in columnas_archivo for col in columnas_requeridas):
            st.error(f"El archivo 'data/HorariosReuniones.xlsx' no contiene las columnas mínimas esperadas.\nColumnas encontradas: {list(df_horarios.columns)}")
        else:
            col1, col2, col3 = st.columns(3)
            proyecto = col1.selectbox("Proyecto", ["Todos"] + sorted(df_horarios["PROYECTO"].dropna().unique().tolist()))
            gerente = col2.selectbox("Gerente", ["Todos"] + sorted(df_horarios["GERENTE"].dropna().unique().tolist()))
            tipo_reunion = col3.selectbox("Tipo de Reunión", ["Todos", "Intermedia", "Semanal"])

            df_filtrado = df_horarios.copy()

            if proyecto != "Todos":
                df_filtrado = df_filtrado[df_filtrado["PROYECTO"] == proyecto]
            if gerente != "Todos":
                df_filtrado = df_filtrado[df_filtrado["GERENTE"] == gerente]

            # Mostrar solo columnas relevantes según el tipo de reunión
            if tipo_reunion == "Intermedia":
                df_filtrado = df_filtrado[["SUCURSAL", "PRACTICANTE", "GERENTE", "PROYECTO", "DIA INTERMEDIA", "HORA INTERMEDIA"]]
            elif tipo_reunion == "Semanal":
                df_filtrado = df_filtrado[["SUCURSAL", "PRACTICANTE", "GERENTE", "PROYECTO", "DIA SEMANAL", "HORA SEMANAL"]]

            st.dataframe(df_filtrado, use_container_width=True)
            st.markdown(descargar_excel(df_filtrado, "HorarioReuniones_filtrado.xlsx"), unsafe_allow_html=True)

    else:
        st.warning("No se pudo cargar el archivo 'HorariosReuniones.xlsx'.")
