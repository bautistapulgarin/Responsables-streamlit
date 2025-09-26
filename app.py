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
    :root{
        --blue-dark: #0a3d62;
        --blue-mid: #1f4e79;
        --blue-light: #eaf3fb;
        --neutral: #6b7a86;
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
    /* Select / Textarea / DataFrame */
    .stSelectbox, .stTextArea, .stDataFrame {
        border-radius: 10px;
    }
    textarea {
        border-radius: 8px !important;
        border: 1px solid var(--blue-mid) !important;
        font-family: monospace !important;
    }
    /* Encabezado */
    .header-row {
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Encabezado con logo (pequeño)
# ----------------------------
col_title, col_logo = st.columns([6, 1])
with col_title:
    st.title("Consulta de Responsables de Proyectos")
with col_logo:
    # Logo reducido; cambia width si quieres más pequeño (ej: 90)
    st.image("loading.png", width=100)

# ----------------------------
# Carga de datos
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

df = load_data()

# ----------------------------
# Inicializar session_state para los filtros
# ----------------------------
for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
    if filtro not in st.session_state:
        st.session_state[filtro] = "Todos"

# Botón para restablecer filtros
st.markdown("---")
if st.button("Restablecer filtros"):
    for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado"]:
        st.session_state[filtro] = "Todos"

# ----------------------------
# Filtros en una fila
# ----------------------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    sucursal = st.selectbox(
        "Sucursal",
        ["Todos"] + sorted(df["Sucursal"].dropna().unique().tolist()),
        key="sucursal",
    )
with col2:
    cluster = st.selectbox(
        "Cluster",
        ["Todos"] + sorted(df["Cluster"].dropna().unique().tolist()),
        key="cluster",
    )
with col3:
    proyecto = st.selectbox(
        "Proyecto",
        ["Todos"] + sorted(df["Proyecto"].dropna().unique().tolist()),
        key="proyecto",
    )
with col4:
    cargo = st.selectbox(
        "Cargo",
        ["Todos"] + sorted(df["Cargo"].dropna().unique().tolist()),
        key="cargo",
    )
with col5:
    estado = st.selectbox(
        "Estado",
        ["Todos"] + sorted(df["Estado"].dropna().unique().tolist()),
        key="estado",
    )

# ----------------------------
# Aplicar filtros
# ----------------------------
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

# ----------------------------
# Resultados y área de correos
# ----------------------------
st.markdown("---")
st.subheader("Resultados de la consulta")

if not df_filtrado.empty:
    st.dataframe(
        df_filtrado[
            [
                "Sucursal",
                "Cluster",
                "Proyecto",
                "HC",
                "Cargo",
                "Responsable",
                "FechaIngreso",
                "Estado",
                "Correo",
                "Celular",
            ]
        ],
        use_container_width=True,
    )

    # Preparo la cadena de correos
    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)

    col_text, col_copy = st.columns([5, 1])
    with col_text:
        st.text_area("Correos", value=correos_str, height=200, key="correos_textarea")
    with col_copy:
        if correos_str.strip():
            correos_json = json.dumps(correos_str)
            # HTML/JS que copia al portapapeles o permite seleccionar
            html = f"""
            <div style="font-family: Arial, sans-serif;">
              <div style="display:flex; flex-direction:column; gap:10px;">
                <button id="copy-btn" style="
                    width:100%;
                    padding:10px;
                    font-size:14px;
                    background-color:#1f4e79;
                    color:#ffffff;
                    border:none;
                    border-radius:8px;
                    font-weight:600;
                ">Copiar</button>

                <button id="select-btn" style="
                    width:100%;
                    padding:10px;
                    font-size:14px;
                    background-color:white;
                    color:#1f4e79;
                    border:1px solid #1f4e79;
                    border-radius:8px;
                    font-weight:600;
                ">Seleccionar (Ctrl+C)</button>

                <div id="msg" style="height:18px; font-size:13px; color:#0a3d62;"></div>

                <textarea id="hidden-ta" style="
                    display:none;
                    width:100%;
                    height:140px;
                    border-radius:8px;
                    border:1px solid #1f4e79;
                    padding:8px;
                    font-family: monospace;
                    resize: none;
                " readonly></textarea>
              </div>

              <script>
                const text = {correos_json};
                const copyBtn = document.getElementById("copy-btn");
                const selectBtn = document.getElementById("select-btn");
                const msg = document.getElementById("msg");
                const ta = document.getElementById("hidden-ta");

                copyBtn.addEventListener("click", async () => {{
                  try {{
                    await navigator.clipboard.writeText(text);
                    msg.innerText = "Copiado";
                  }} catch (e) {{
                    // Fallback: usar textarea temporal dentro del iframe
                    try {{
                      ta.style.display = "block";
                      ta.value = text;
                      ta.select();
                      document.execCommand('copy');
                      ta.style.display = "none";
                      msg.innerText = "Copiado (fallback)";
                    }} catch (ee) {{
                      msg.innerText = "No fue posible copiar automáticamente. Use 'Seleccionar' y Ctrl+C.";
                    }}
                  }}
                  setTimeout(()=>msg.innerText = "", 2500);
                }});

                selectBtn.addEventListener("click", () => {{
                  ta.style.display = "block";
                  ta.value = text;
                  ta.focus();
                  ta.select();
                  msg.innerText = "Texto seleccionado. Presione Ctrl+C";
                  setTimeout(()=>msg.innerText = "", 4000);
                }});
              </script>
            </div>
            """
            components.html(html, height=220)
        else:
            st.write("No hay correos para copiar.")
else:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
