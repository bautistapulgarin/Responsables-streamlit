# ==========================================================
# APP DE SEGUIMIENTO DE PROYECTOS Y HORARIOS DE REUNIONES
# ==========================================================

import streamlit as st
import pandas as pd
import io
import base64
import unicodedata

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

# -----------------------------
# FUNCIONES AUXILIARES
# -----------------------------
def normalizar_texto(texto):
    """Normaliza texto eliminando tildes, mayúsculas y espacios."""
    texto = str(texto).strip().upper()
    texto = "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")
    return texto


def descargar_excel(df, nombre_archivo):
    """Permite descargar un DataFrame en formato Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:  # se usa openpyxl para compatibilidad en la nube
        df.to_excel(writer, index=False)
    datos = output.getvalue()
    b64 = base64.b64encode(datos).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar {nombre_archivo}</a>'
    return href


def cargar_excel(nombre_archivo, columnas_esperadas):
    """Carga un archivo Excel verificando las columnas requeridas (tolerante a tildes y mayúsculas)."""
    try:
        df = pd.read_excel(nombre_archivo)
        df.columns = [normalizar_texto(c) for c in df.columns]
        columnas_esperadas_norm = [normalizar_texto(c) for c in columnas_esperadas]

        if not all(col in df.columns for col in columnas_esperadas_norm):
            st.error(
                f"⚠️ El archivo '{nombre_archivo}' no contiene las columnas esperadas.\n\n"
                f"Columnas encontradas: {list(df.columns)}"
            )
            return None
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo '{nombre_archivo}': {e}")
        return None


# -----------------------------
# INTERFAZ PRINCIPAL
# -----------------------------
tabs = st.tabs([
    "📋 Consulta de Responsables",
    "📊 Reporte de Avances",
    "🕒 Horario de Reuniones"
])

# ==========================================================
# PESTAÑA 1: CONSULTA DE RESPONSABLES
# ==========================================================
with tabs[0]:
    st.header("📋 Consulta de Responsables de Proyecto")

    columnas_esperadas_resp = [
        "SUCURSAL", "CLUSTER", "PROYECTO", "CARGO",
        "ESTADO", "GERENTE DE PROYECTO", "CORREO", "RESPONSABLE"
    ]

    df_resp = cargar_excel("data/ResponsablesPorProyecto.xlsx", columnas_esperadas_resp)

    if df_resp is not None:
        # Filtros
        sucursal = st.selectbox("Sucursal:", ["Todos"] + sorted(df_resp["SUCURSAL"].dropna().unique().tolist()))
        cluster = st.selectbox("Cluster:", ["Todos"] + sorted(df_resp["CLUSTER"].dropna().unique().tolist()))
        proyecto = st.selectbox("Proyecto:", ["Todos"] + sorted(df_resp["PROYECTO"].dropna().unique().tolist()))
        cargo = st.selectbox("Cargo:", ["Todos"] + sorted(df_resp["CARGO"].dropna().unique().tolist()))
        estado = st.selectbox("Estado:", ["Todos"] + sorted(df_resp["ESTADO"].dropna().unique().tolist()))
        gerente = st.selectbox("Gerente de Proyecto:", ["Todos"] + sorted(df_resp["GERENTE DE PROYECTO"].dropna().unique().tolist()))
        campo_abierto = st.text_input("🔎 Búsqueda libre (por nombre, correo, cargo, etc.):")

        # Aplicar filtros
        df_filtrado = df_resp.copy()

        if sucursal != "Todos":
            df_filtrado = df_filtrado[df_filtrado["SUCURSAL"] == sucursal]
        if cluster != "Todos":
            df_filtrado = df_filtrado[df_filtrado["CLUSTER"] == cluster]
        if proyecto != "Todos":
            df_filtrado = df_filtrado[df_filtrado["PROYECTO"] == proyecto]
        if cargo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["CARGO"] == cargo]
        if estado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["ESTADO"] == estado]
        if gerente != "Todos":
            df_filtrado = df_filtrado[df_filtrado["GERENTE DE PROYECTO"] == gerente]
        if campo_abierto:
            df_filtrado = df_filtrado[df_filtrado.apply(lambda row: campo_abierto.lower() in row.to_string().lower(), axis=1)]

        st.dataframe(df_filtrado, use_container_width=True)
        st.markdown(descargar_excel(df_filtrado, "ResponsablesFiltrados.xlsx"), unsafe_allow_html=True)
    else:
        st.warning("⚠️ No se pudo cargar la información de responsables.")


# ==========================================================
# PESTAÑA 2: REPORTE DE AVANCES
# ==========================================================
with tabs[1]:
    st.header("📊 Reporte de Avances")
    try:
        df_avances = pd.read_excel("data/ReporteAvances.xlsx")
        st.dataframe(df_avances, use_container_width=True)
        st.markdown(descargar_excel(df_avances, "ReporteAvances.xlsx"), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ Error al cargar el archivo de avances: {e}")


# ==========================================================
# PESTAÑA 3: HORARIO DE REUNIONES
# ==========================================================
with tabs[2]:
    st.header("🕒 Horario de Reuniones - Last Planner System")

    columnas_esperadas_horarios = [
        "SUCURSAL",
        "PRACTICANTE",
        "GERENTE",
        "PROYECTO",
        "DIA INTERMEDIA",
        "HORA INTERMEDIA",
        "DIA SEMANAL",
        "HORA SEMANAL"
    ]

    df_horarios = cargar_excel("data/HorariosReuniones.xlsx", columnas_esperadas_horarios)

    if df_horarios is not None:
        st.success("✅ Archivo de horarios cargado correctamente.")

        # Filtros
        sucursales = ["Todos"] + sorted(df_horarios["SUCURSAL"].dropna().unique().tolist())
        proyectos = ["Todos"] + sorted(df_horarios["PROYECTO"].dropna().unique().tolist())
        gerentes = ["Todos"] + sorted(df_horarios["GERENTE"].dropna().unique().tolist())
        tipo_reunion = st.radio("Tipo de Reunión:", ["Intermedia", "Semanal"])

        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_sucursal = st.selectbox("Sucursal:", sucursales)
        with col2:
            filtro_proyecto = st.selectbox("Proyecto:", proyectos)
        with col3:
            filtro_gerente = st.selectbox("Gerente:", gerentes)

        df_filtrado = df_horarios.copy()

        if filtro_sucursal != "Todos":
            df_filtrado = df_filtrado[df_filtrado["SUCURSAL"] == filtro_sucursal]
        if filtro_proyecto != "Todos":
            df_filtrado = df_filtrado[df_filtrado["PROYECTO"] == filtro_proyecto]
        if filtro_gerente != "Todos":
            df_filtrado = df_filtrado[df_filtrado["GERENTE"] == filtro_gerente]

        if tipo_reunion == "Intermedia":
            columnas_mostrar = ["SUCURSAL", "GERENTE", "PROYECTO", "DIA INTERMEDIA", "HORA INTERMEDIA"]
        else:
            columnas_mostrar = ["SUCURSAL", "GERENTE", "PROYECTO", "DIA SEMANAL", "HORA SEMANAL"]

        st.dataframe(df_filtrado[columnas_mostrar], use_container_width=True)
        st.markdown(descargar_excel(df_filtrado[columnas_mostrar], "HorariosFiltrados.xlsx"), unsafe_allow_html=True)
    else:
        st.warning("⚠️ No se pudo cargar la información de horarios.")
