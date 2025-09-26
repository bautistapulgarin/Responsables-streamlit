import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")
st.title("📊 Consulta de Responsables de Proyectos")

@st.cache_data
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# Inicializar session_state para los filtros
for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
    if filtro not in st.session_state:
        st.session_state[filtro] = "Todos"

# Botón para restablecer filtros
if st.button("🔄 Restablecer filtros"):
    st.session_state["sucursal"] = "Todos"
    st.session_state["cluster"] = "Todos"
    st.session_state["proyecto"] = "Todos"
    st.session_state["cargo"] = "Todos"
    st.session_state["estado"] = "Todos"

# Filtros en columnas
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    sucursal = st.selectbox("Sucursal", ["Todos"] + sorted(df["Sucursal"].dropna().unique().tolist()), key="sucursal")
with col2:
    cluster = st.selectbox("Cluster", ["Todos"] + sorted(df["Cluster"].dropna().unique().tolist()), key="cluster")
with col3:
    proyecto = st.selectbox("Proyecto", ["Todos"] + sorted(df["Proyecto"].dropna().unique().tolist()), key="proyecto")
with col4:
    cargo = st.selectbox("Cargo", ["Todos"] + sorted(df["Cargo"].dropna().unique().tolist()), key="cargo")
with col5:
    estado = st.selectbox("Estado", ["Todos"] + sorted(df["Estado"].dropna().unique().tolist()), key="estado")

# Aplicar filtros
df_filtrado = df.copy()
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

st.subheader("🔍 Resultados de la consulta")
if not df_filtrado.empty:
    st.dataframe(df_filtrado[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]])

    # Campo de texto para copiar los correos
    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)
    st.text_area("📋 Copiar todos los correos desde aquí", value=correos_str, height=200)
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
