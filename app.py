import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os

st.title("📊 Consulta de Responsables por Proyecto")

# ===============================
# 🔹 Debug: Archivos disponibles
# ===============================
st.sidebar.header("Debug: Archivos en la raíz")
st.sidebar.write(os.listdir())

# ===============================
# 🔹 Cargar datos
# ===============================
@st.cache_data
def load_data():
    # Asegúrate de que tu archivo esté en la raíz del repo
    return pd.read_excel("ResponsablesPorProyecto.xlsx")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'ResponsablesPorProyecto.xlsx'. Asegúrate de subirlo al repositorio en la raíz.")
    st.stop()

# ===============================
# 🔹 Filtros con reset
# ===============================
st.sidebar.header("Filtros")

if "reset" not in st.session_state:
    st.session_state.reset = False

# Botón para restablecer filtros
if st.sidebar.button("🔄 Restablecer filtros"):
    st.session_state.reset = True
else:
    st.session_state.reset = False

if st.session_state.reset:
    sucursal = cluster = proyecto = cargo = None
else:
    sucursal = st.sidebar.selectbox("Sucursal", [""] + sorted(df["Sucursal"].dropna().unique()))
    cluster = st.sidebar.selectbox("Cluster", [""] + sorted(df["Cluster"].dropna().unique()))
    proyecto = st.sidebar.selectbox("Proyecto", [""] + sorted(df["Proyecto"].dropna().unique()))
    cargo = st.sidebar.selectbox("Cargo", [""] + sorted(df["Cargo"].dropna().unique()))

filtro = df.copy()
if sucursal:
    filtro = filtro[filtro["Sucursal"] == sucursal]
if cluster:
    filtro = filtro[filtro["Cluster"] == cluster]
if proyecto:
    filtro = filtro[filtro["Proyecto"] == proyecto]
if cargo:
    filtro = filtro[filtro["Cargo"] == cargo]

# ===============================
# 🔹 Campo de búsqueda libre
# ===============================
st.subheader("🔎 Consulta libre en lenguaje natural")
pregunta = st.text_input("Ejemplo: 'quién es el Director de obra del proyecto Burdeos Ciudad La Salle'")

def responder_pregunta(pregunta):
    pregunta = pregunta.lower()
    temp = df.copy()

    # Buscar proyecto
    for p in df["Proyecto"].unique():
        if p.lower() in pregunta:
            temp = temp[temp["Proyecto"].str.lower() == p.lower()]
            break

    # Buscar sucursal
    for s in df["Sucursal"].unique():
        if s.lower() in pregunta:
            temp = temp[temp["Sucursal"].str.lower() == s.lower()]
            break

    # Buscar cluster
    for c in df["Cluster"].unique():
        if c.lower() in pregunta:
            temp = temp[temp["Cluster"].str.lower() == c.lower()]
            break

    # Buscar cargo
    for c in df["Cargo"].unique():
        if c.lower() in pregunta:
            temp = temp[temp["Cargo"].str.lower() == c.lower()]
            break

    # Buscar responsable
    for r in df["Responsable"].unique():
        if r.lower() in pregunta:
            temp = temp[temp["Responsable"].str.lower() == r.lower()]
            break

    if temp.empty:
        return "❌ No se encontraron resultados para tu consulta."

    return temp

# ===============================
# 🔹 Resultados
# ===============================
if pregunta:
    resultados = responder_pregunta(pregunta)
    if isinstance(resultados, pd.DataFrame):
        st.success("✅ Resultados encontrados con consulta libre")
        st.dataframe(resultados)
        filtro = resultados  # Para botón copiar correos
    else:
        st.warning(resultados)
elif not filtro.empty:
    st.success("✅ Resultados por filtros")
    st.dataframe(filtro)
else:
    st.info("Usa los filtros de la izquierda o escribe una consulta arriba.")

# ===============================
# 🔹 Botón para copiar correos al portapapeles
# ===============================
if not filtro.empty:
    correos = "; ".join(filtro["Correo"].dropna().unique())
    if st.button("📋 Copiar correos al portapapeles"):
        components.html(
            f"""
            <script>
            navigator.clipboard.writeText("{correos}");
            alert("¡Correos copiados al portapapeles!");
            </script>
            """,
            height=0,
        )
