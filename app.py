import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")

# ---- Estilos personalizados ----
st.markdown(
    """
    <style>
        .main {
            background-color: #f5f9ff;
        }
        .stButton>button {
            background-color: #1f4e79;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #163754;
        }
        .stSelectbox, .stTextArea, .stDataFrame {
            border-radius: 10px;
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Encabezado con título y logo ----
col_title, col_logo = st.columns([6, 1])
with col_title:
    st.title("Consulta de Responsables de Proyectos")
with col_logo:
    st.image("loading.png", width=120)  # 🔹 Logo reducido

# ---- Cargar datos ----
@st.cache_data
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# ---- Inicializar session_state para los filtros ----
for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
    if filtro not in st.session_state:
        st.session_state[filtro] = "Todos"

# ---- Botón para restablecer filtros ----
if st.button("Restablecer filtros"):
    for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
        st.session_state[filtro] = "Todos"

# ---- Filtros en columnas ----
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

# ---- Aplicar filtros ----
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

# ---- Resultados ----
st.subheader("Resultados de la consulta")
if not df_filtrado.empty:
    st.dataframe(
        df_filtrado[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]],
        use_container_width=True
    )

    # Campo de texto para copiar los correos
    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)
    col_text, col_copy = st.columns([5, 1])
    with col_text:
        st.text_area("Correos", value=correos_str, height=200, key="correos_textarea")
    with col_copy:
        if st.button("Copiar correos"):
            st.session_state["copied"] = correos_str
            st.success("Copiado en el portapapeles (usa Ctrl+C en el campo).")
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")

