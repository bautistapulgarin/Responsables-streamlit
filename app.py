import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# ----------------------------
# Configuración y estilos
# ----------------------------
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")

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

    :root{
        --blue-dark: #0a3d62;
        --blue-mid: #1f4e79;
        --blue-light: #eaf3fb;
    }
    /* Fondo */
    .reportview-container, .main {
        background-color: var(--blue-light);
    }
    /* Títulos */
    .css-1d391kg h1, .css-1d391kg h2 {
        color: var(--blue-dark);
        font-family: "Arial", sans-serif;
    }
    /* Botones Streamlit */
    .stButton>button {
        background-color: var(--blue-mid);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 12px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #163754;
    }
    /* Select / DataFrame */
    .stSelectbox, .stDataFrame {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Encabezado con logo
# ----------------------------
col_title, col_logo = st.columns([6, 1])
with col_title:
    st.title("Consulta de Responsables de Proyectos")
with col_logo:
    st.image("loading.png", width=100)

# ----------------------------
# Carga de datos
# ----------------------------
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# ----------------------------
# Inicializar session_state
# ----------------------------
for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
    if filtro not in st.session_state:
        st.session_state[filtro] = []

# Botón para restablecer filtros
st.markdown("---")
if st.button("Restablecer filtros"):
    for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
        st.session_state[filtro] = []

# ----------------------------
# Filtros en una fila (multiselect)
# ----------------------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    sucursal = st.multiselect("Sucursal", sorted(df["Sucursal"].dropna().unique().tolist()), key="sucursal")
with col2:
    cluster = st.multiselect("Cluster", sorted(df["Cluster"].dropna().unique().tolist()), key="cluster")
with col3:
    proyecto = st.multiselect("Proyecto", sorted(df["Proyecto"].dropna().unique().tolist()), key="proyecto")
with col4:
    cargo = st.multiselect("Cargo", sorted(df["Cargo"].dropna().unique().tolist()), key="cargo")
with col5:
    estado = st.multiselect("Estado", sorted(df["Estado"].dropna().unique().tolist()), key="estado")

# ----------------------------
# Aplicar filtros
# ----------------------------
df_filtrado = df.copy()
if sucursal:
    df_filtrado = df_filtrado[df_filtrado["Sucursal"].isin(sucursal)]
if cluster:
    df_filtrado = df_filtrado[df_filtrado["Cluster"].isin(cluster)]
if proyecto:
    df_filtrado = df_filtrado[df_filtrado["Proyecto"].isin(proyecto)]
if cargo:
    df_filtrado = df_filtrado[df_filtrado["Cargo"].isin(cargo)]
if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]

# ----------------------------
# Resultados y botón copiar
# ----------------------------
st.markdown("---")
st.subheader("Resultados de la consulta")

if not df_filtrado.empty:
    st.dataframe(
        df_filtrado[
            ["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable",
             "FechaIngreso", "Estado", "Correo", "Celular"]
        ],
        use_container_width=True,
    )

    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)

    if correos_str.strip():
        correos_json = json.dumps(correos_str)
        html = f"""
        <div style="font-family: Arial, sans-serif; margin-top:15px;">
          <button id="copy-btn" style="
              padding:10px 16px;
              font-size:14px;
              background-color:#1f4e79;
              color:#ffffff;
              border:none;
              border-radius:8px;
              font-weight:600;
              cursor:pointer;
          ">Copiar correos</button>
          <div id="msg" style="height:18px; font-size:13px; color:#0a3d62; margin-top:6px;"></div>

          <script>
            const text = {correos_json};
            const copyBtn = document.getElementById("copy-btn");
            const msg = document.getElementById("msg");

            copyBtn.addEventListener("click", async () => {{
              try {{
                await navigator.clipboard.writeText(text);
                msg.innerText = "Copiado";
              }} catch (e) {{
                try {{
                  const ta = document.createElement("textarea");
                  ta.value = text;
                  document.body.appendChild(ta);
                  ta.select();
                  document.execCommand('copy');
                  document.body.removeChild(ta);
                  msg.innerText = "Copiado (fallback)";
                }} catch (ee) {{
                  msg.innerText = "No fue posible copiar automáticamente. Use Ctrl+C.";
                }}
              }}
              setTimeout(()=>msg.innerText = "", 2500);
            }});
          </script>
        </div>
        """
        components.html(html, height=100)
    else:
        st.write("No hay correos para copiar.")
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
