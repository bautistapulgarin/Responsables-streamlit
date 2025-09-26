import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")

# Forzar fondo blanco
st.markdown(
    """
    <style>
        body {
            background-color: white !important;
            color: black !important;
        }
        .stApp {
            background-color: white !important;
        }
        /* Estética general en azules sobrios */
        .block-container {
            padding-top: 1rem;
        }
        h1, h2, h3, h4, h5 {
            color: #0A2540; /* Azul oscuro elegante */
        }
        .stSelectbox label {
            color: #0A2540;
            font-weight: 600;
        }
        .stDataFrame {
            border: 1px solid #1E3A8A;
            border-radius: 12px;
            overflow: hidden;
        }
        .stButton button {
            background-color: #1E3A8A;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.6em 1.2em;
            font-weight: 600;
        }
        .stButton button:hover {
            background-color: #3B82F6; /* Azul más claro al pasar */
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cargar datos SIEMPRE actualizados (sin cache)
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# Logo en la esquina superior derecha
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("loading.png", width=90)  # Logo más pequeño
with col_title:
    st.title("Consulta de Responsables de Proyectos")

# Inicializar session_state para filtros
for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
    if filtro not in st.session_state:
        st.session_state[filtro] = "Todos"

# Botón para restablecer filtros
if st.button("Restablecer filtros"):
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

# Resultados
st.subheader("Resultados de la consulta")
if not df_filtrado.empty:
    st.dataframe(
        df_filtrado[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]],
        use_container_width=True
    )

    # Campo de texto con correos y botón de copiar
    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)

    col_correos, col_boton = st.columns([6, 1])
    with col_correos:
        st.text_area("Correos", value=correos_str, height=200)
    with col_boton:
        st.download_button(
            "Copiar correos",
            data=correos_str,
            file_name="correos.txt",
            mime="text/plain"
        )

else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
