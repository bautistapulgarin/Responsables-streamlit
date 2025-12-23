import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# ======================================================
# CONFIGURACIÓN GENERAL (DEBE SER LO PRIMERO)
# ======================================================
st.set_page_config(
    page_title="Consulta de Responsables de Proyectos",
    layout="wide",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

# ======================================================
# MÁSCARA DE CARGA INICIAL (ANTICIPA EL RENDER)
# ======================================================
st.markdown("""
<style>
#startup-mask {
    position: fixed;
    inset: 0;
    background-color: #eaf3fb;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Spinner */
.startup-loader {
    width: 54px;
    height: 54px;
    border: 5px solid #d6e4f0;
    border-top: 5px solid #1f4e79;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>

<div id="startup-mask">
    <div class="startup-loader"></div>
</div>

<script>
setTimeout(() => {
    const mask = document.getElementById("startup-mask");
    if (mask) mask.remove();
}, 900);
</script>
""", unsafe_allow_html=True)

# ======================================================
# CSS GLOBAL (INYECTAR UNA SOLA VEZ)
# ======================================================
st.markdown("""
<style>
/* ===== OCULTAR ELEMENTOS NATIVOS STREAMLIT ===== */
#MainMenu,
header,
footer,
.stDeployButton,
[data-testid="stToolbar"],
[data-testid="baseButton-header"],
[data-testid="stHeader"],
[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* ===== BASE VISUAL CORPORATIVA ===== */
html, body, .stApp {
    background-color: #eaf3fb !important;
    color: #0a3d62;
}

/* ===== VARIABLES DE COLOR ===== */
:root {
    --blue-dark: #0a3d62;
    --blue-mid: #1f4e79;
    --blue-light: #eaf3fb;
}

/* ===== BOTONES ===== */
.stButton > button {
    background-color: var(--blue-mid);
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #163754;
}

/* ===== INPUTS ===== */
input, textarea {
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN
# ======================================================
def login_screen():

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("loading.png", width=120)

        st.markdown(
            "<h2 style='text-align:center; margin-top:10px;'>Acceso al Sistema</h2>",
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar")

        if submit:
            if password == st.secrets["password"]:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

# ======================================================
# APP PRINCIPAL
# ======================================================
def main_app():

    col_title, col_logo = st.columns([6, 1])

    with col_title:
        st.title("Consulta de Responsables de Proyectos")

    with col_logo:
        st.image("loading.png", width=80)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📜 Directorio Documental",
        "🧑🏿 Responsables por Proyecto",
        "📈 Reporte de Avances",
        "🕰️ Horario Reuniones LP",
        "📋 Formulario",
        "🏢 Proyectos en grilla",
        "📅 Cronograma de visitas",
        "⏱️ Pull Planning"
    ])

    with tab1:
        st.info("Contenido del Directorio Documental")

    with tab2:
        st.info("Contenido de Responsables por Proyecto")

    with tab3:
        st.info("Contenido del Reporte de Avances")

    with tab4:
        st.info("Contenido del Horario de Reuniones LP")

    with tab5:
        st.info("Contenido del Formulario")

    with tab6:
        st.info("Contenido de Proyectos en grilla")

    with tab7:
        st.info("Contenido del Cronograma de visitas")

    with tab8:
        st.info("Contenido de Pull Planning")

# ======================================================
# EJECUCIÓN PRINCIPAL
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
