import streamlit as st
import pandas as pd


# Configurar la página para que abra en modo ancho
st.set_page_config(
    page_title="Consulta de Responsables de Proyectos",
    layout="wide"  # Esto activa el modo wide
)



st.title("📊 Consulta de Responsables de Proyectos")

@st.cache_data
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# Crear columnas para los filtros
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    sucursal = st.selectbox("Sucursal", ["Todos"] + sorted(df["Sucursal"].dropna().unique().tolist()))
with col2:
    cluster = st.selectbox("Cluster", ["Todos"] + sorted(df["Cluster"].dropna().unique().tolist()))
with col3:
    proyecto = st.selectbox("Proyecto", ["Todos"] + sorted(df["Proyecto"].dropna().unique().tolist()))
with col4:
    cargo = st.selectbox("Cargo", ["Todos"] + sorted(df["Cargo"].dropna().unique().tolist()))
with col5:
    estado = st.selectbox("Estado", ["Todos"] + sorted(df["Estado"].dropna().unique().tolist()))

# Aplicar filtros
if sucursal != "Todos":
    df = df[df["Sucursal"] == sucursal]
if cluster != "Todos":
    df = df[df["Cluster"] == cluster]
if proyecto != "Todos":
    df = df[df["Proyecto"] == proyecto]
if cargo != "Todos":
    df = df[df["Cargo"] == cargo]
if estado != "Todos":
    df = df[df["Estado"] == estado]

st.subheader("🔍 Resultados de la consulta")
if not df.empty:
    st.dataframe(df[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]])
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
