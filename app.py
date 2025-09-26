import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")

# Estilos CSS personalizados (colores sobrios, escala de azules, bordes redondeados)
st.markdown("""
    <style>
        /* Fondo general */
        .main {
            background-color: #f4f8fb;
        }
        /* Títulos */
        h1, h2, h3, h4 {
            color: #0a3d62;
            font-family: 'Arial', sans-serif;
        }
        /* Selectbox y botones */
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 8px;
            border: 1px solid #0a3d62;
        }
        .stButton button {
            background-color: #0a3d62;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #3c6382;
            color: white;
        }
        /* Dataframe */
        .stDataFrame {
            border-radius: 12px;
            border: 1px solid #3c6382;
        }
        /* Textarea */
        textarea {
            border-radius: 8px !important;
            border: 1px solid #3c6382 !important;
            font-family: monospace !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA CON LOGO ---
header_col1, header_col2 = st.columns([6,1])
with header_col1:
    st.title("Consulta de Responsables de Proyectos")
with header_col2:
    st.image("loading.png", use_container_width=True)  # Logo actualizado

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# Inicializar session_state para los filtros
for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
    if filtro not in st.session_state:
        st.session_state[filtro] = "Todos"

# Botón para restablecer filtros
st.markdown("---")
if st.button("Restablecer filtros"):
    for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
        st.session_state[filtro] = "Todos"

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

# --- RESULTADOS ---
st.markdown("---")
st.subheader("Resultados de la consulta")

if not df_filtrado.empty:
    st.dataframe(
        df_filtrado[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]],
        use_container_width=True
    )

    # Campo de texto + botón copiar
    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)

    col_text, col_button = st.columns([5, 1])
    with col_text:
        st.text_area("Correos", value=correos_str, height=200, key="correos_area")
    with col_button:
        if correos_str.strip():
            correos_json = json.dumps(correos_str)
            html = f"""
            <div style="display:flex; flex-direction:column; align-items:center; gap:8px;">
              <button id="copy-btn" style="width:100%; padding:10px; font-size:14px;
                background-color:#0a3d62; color:white; border:none; border-radius:8px; font-weight:bold;">
                Copiar
              </button>
              <div id="msg" style="font-size:13px;color:green;height:18px;"></div>
            </div>
            <script>
              const text = {correos_json};
              const btn = document.getElementById('copy-btn');
              btn.addEventListener('click', async () => {{
                try {{
                  await navigator.clipboard.writeText(text);
                  document.getElementById('msg').innerText = 'Copiado';
                }} catch (err) {{
                  const ta = document.createElement('textarea');
                  ta.value = text;
                  document.body.appendChild(ta);
                  ta.select();
                  document.execCommand('copy');
                  document.body.removeChild(ta);
                  document.getElementById('msg').innerText = 'Copiado';
                }}
                setTimeout(()=>document.getElementById('msg').innerText='',2000);
              }});
            </script>
            """
            components.html(html, height=100)
        else:
            st.write("No hay correos para copiar.")
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")

