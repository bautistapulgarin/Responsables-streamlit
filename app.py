import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_excel("ResponsablesPorProyecto.xlsx")

df = load_data()

st.title("📊 Consulta de Responsables por Proyecto")

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
    sucursal = st.sidebar.selectbox("Sucursal", [""] + sorted(df["Sucursal"].unique()))
    cluster = st.sidebar.selectbox("Cluster", [""] + sorted(df["Cluster"].unique()))
    proyecto = st.sidebar.selectbox("Proyecto", [""] + sorted(df["Proyecto"].unique()))
    cargo = st.sidebar.selectbox("Cargo", [""] + sorted(df["Cargo"].unique()))

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

    if "proyecto" in pregunta:
        for p in df["Proyecto"].unique():
            if p.lower() in pregunta:
                temp = df[df["Proyecto"].str.lower() == p.lower()]
                break
        else:
            return "❌ Proyecto no encontrado."
    elif "sucursal" in pregunta:
        for s in df["Sucursal"].unique():
            if s.lower() in pregunta:
                temp = df[df["Sucursal"].str.lower() == s.lower()]
                break
        else:
            return "❌ Sucursal no encontrada."
    elif "cluster" in pregunta:
        for c in df["Cluster"].unique():
            if c.lower() in pregunta:
                temp = df[df["Cluster"].str.lower() == c.lower()]
                break
        else:
            return "❌ Cluster no encontrado."
    elif "gerencia" in pregunta or "gerente" in pregunta:
        for g in df["Responsable"].unique():
            if g.lower() in pregunta:
                temp = df[df["Responsable"].str.lower() == g.lower()]
                break
        else:
            return "❌ Gerencia/Gerente no encontrado."
    else:
        return "❌ No entendí la pregunta (usa palabras como proyecto, sucursal, cluster o gerente)."

    # Buscar cargo
    cargo_encontrado = None
    for c in df["Cargo"].unique():
        if c.lower() in pregunta:
            cargo_encontrado = c
            break

    if cargo_encontrado:
        temp = temp[temp["Cargo"].str.lower() == cargo_encontrado.lower()]

    if temp.empty:
        return "❌ No se encontraron resultados."

    return temp

# ===============================
# 🔹 Resultados
# ===============================
if pregunta:
    resultados = responder_pregunta(pregunta)
    if isinstance(resultados, pd.DataFrame):
        st.success("✅ Resultados encontrados con consulta libre")
        st.dataframe(resultados)
        filtro = resultados  # Para que el botón copiar correos funcione también
    else:
        st.warning(resultados)
elif not filtro.empty:
    st.success("✅ Resultados por filtros")
    st.dataframe(filtro)
else:
    st.info("Usa los filtros de la izquierda o escribe una consulta arriba.")

# ===============================
# 🔹 Botón para copiar correos
# ===============================
if not filtro.empty:
    correos = "; ".join(filtro["Correo"].dropna().unique())

    # Botón que dispara copia al portapapeles
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

