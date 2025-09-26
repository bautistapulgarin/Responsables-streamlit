import streamlit as st
import pandas as pd

st.title("📊 Consulta de Responsables de Proyectos")

# Función para cargar datos desde el Excel en el repo
@st.cache_data
def load_data():
    return pd.read_excel("data/responsables.xlsx")

df = load_data()

# Selectores dinámicos
sucursal = st.selectbox("Seleccione la Sucursal", ["Todos"] + sorted(df["Sucursal"].dropna().unique().tolist()))
if sucursal != "Todos":
    df = df[df["Sucursal"] == sucursal]

gerencia = st.selectbox("Seleccione la Gerencia", ["Todos"] + sorted(df["Gerencia"].dropna().unique().tolist()))
if gerencia != "Todos":
    df = df[df["Gerencia"] == gerencia]

cluster = st.selectbox("Seleccione el Cluster", ["Todos"] + sorted(df["Cluster"].dropna().unique().tolist()))
if cluster != "Todos":
    df = df[df["Cluster"] == cluster]

proyecto = st.selectbox("Seleccione el Proyecto", ["Todos"] + sorted(df["Proyecto"].dropna().unique().tolist()))
if proyecto != "Todos":
    df = df[df["Proyecto"] == proyecto]

cargo = st.selectbox("Seleccione el Cargo", ["Todos"] + sorted(df["Cargo"].dropna().unique().tolist()))
if cargo != "Todos":
    df = df[df["Cargo"] == cargo]

st.subheader("🔍 Resultados de la consulta")
if not df.empty:
    st.dataframe(df)
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
