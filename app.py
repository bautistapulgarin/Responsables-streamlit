import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

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

st.subheader("🔍 Resultados de la consulta")
if not df_filtrado.empty:
    st.dataframe(df_filtrado[["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable", "FechaIngreso", "Estado", "Correo", "Celular"]])

    # Campo de texto para mostrar los correos
    correos = df_filtrado["Correo"].dropna().tolist()
    correos_str = "\n".join(correos)

    col_text, col_button = st.columns([5, 1])
    with col_text:
        st.text_area("📋 Copiar todos los correos desde aquí", value=correos_str, height=200, key="correos_area")
    with col_button:
        if correos_str.strip():
            # json.dumps asegura que el string quede correctamente escapado para JS
            correos_json = json.dumps(correos_str)
            html = f"""
            <div style="display:flex; flex-direction:column; align-items:center; gap:8px;">
              <button id="copy-btn" style="width:100%; padding:8px; font-size:16px;">📋 Copiar</button>
              <div id="msg" style="font-size:14px;color:green;height:18px;"></div>
            </div>
            <script>
              const text = {correos_json};
              const btn = document.getElementById('copy-btn');
              btn.addEventListener('click', async () => {{
                try {{
                  await navigator.clipboard.writeText(text);
                  document.getElementById('msg').innerText = 'Copiado ✅';
                }} catch (err) {{
                  // Fallback para navegadores que no permitan navigator.clipboard (intenta copy via textarea)
                  try {{
                    const ta = document.createElement('textarea');
                    ta.value = text;
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand('copy');
                    document.body.removeChild(ta);
                    document.getElementById('msg').innerText = 'Copiado (fallback) ✅';
                  }} catch(e) {{
                    document.getElementById('msg').innerText = 'No se pudo copiar automáticamente. Selecciona y presiona Ctrl+C.';
                  }}
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
