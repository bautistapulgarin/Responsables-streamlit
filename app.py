import streamlit as st
import pandas as pd

# Configurar página
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")
st.title("📊 Consulta de Responsables de Proyectos")

@st.cache_data
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# Filtros
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

    # Botón para copiar correos usando HTML/JS
    correos = df["Correo"].dropna().tolist()
    correos_str = ", ".join(correos)  # puedes cambiar a "\n".join(correos) si quieres salto de línea

    if st.button("📋 Copiar todos los correos al portapapeles"):
        st.markdown(f"""
            <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text);
            }}
            copyToClipboard(`{correos_str}`);
            </script>
            """, unsafe_allow_html=True)
        st.success(f"✅ Se copiaron {len(correos)} correos al portapapeles.")
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
