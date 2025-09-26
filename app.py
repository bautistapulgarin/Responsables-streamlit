import streamlit as st
import pandas as pd

st.title("📊 Consulta de Responsables de Proyectos")

@st.cache_data
def load_data():
    # Cambia la ruta si pones el Excel en otra carpeta
    return pd.read_excel("data/responsables.xlsx")

df = load_data()

# Filtros jerárquicos
sucursal = st.selectbox("Sucursal", ["Todos"] + sorted(df["Sucursal"].dropna().unique().tolist()))
if sucursal != "Todos":
    df = df[df["Sucursal"] == sucursal]

cluster = st.selectbox("Cluster", ["Todos"] + sorted(df["Cluster"].dropna().unique().tolist()))
if cluster != "Todos":
    df = df[df["Cluster"] == cluster]

proyecto = st.selectbox("Proyecto", ["Todos"] + sorted(df["Proyecto"].dropna().unique().tolist()))
if proyecto != "Todos":
    df = df[df["Proyecto"] == proyecto]

cargo = st.selectbox("Cargo", ["Todos"] + sorted(df["Cargo"].dropna().unique().tolist()))
if cargo != "Todos":
    df = df[df["Cargo"] == cargo]

estado = st.selectbox("Estado", ["Todos"] + sorted(df["Estado"].dropna().unique().tolist()))
if estado != "Todos":
    df = df[df["Estado"] == estado]

st.subheader("🔍 Resultados de la consulta")
if not df.empty:
    # Mostrar columnas clave
    st.dataframe(df[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]])
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
