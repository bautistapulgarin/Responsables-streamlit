import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# ----------------------------
# Configuración general
# ----------------------------
st.set_page_config(
    page_title="Consulta de Responsables de Proyectos",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ----------------------------
# CSS GLOBAL: Loader + ocultar elementos
# ----------------------------
def inject_global_css():
    st.markdown(
        """
        <style>
        /* ---------- OCULTAR ELEMENTOS STREAMLIT ---------- */
        .stDeployButton {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {display: none !important;}
        #stMainMenu {display: none !important;}
        [data-testid="baseButton-header"] {display: none !important;}

        /* ---------- OVERLAY DE CARGA ---------- */
        #loader-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: white;
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: hideLoader 0.3s ease forwards;
            animation-delay: 0.6s;
        }

        /* Spinner */
        .loader {
            width: 48px;
            height: 48px;
            border: 5px solid #e0e0e0;
            border-top: 5px solid #1f4e79;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes hideLoader {
            to {
                opacity: 0;
                visibility: hidden;
            }
        }
        </style>

        <div id="loader-overlay">
            <div class="loader"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Pantalla de Login
# ----------------------------
def login_screen():

    inject_global_css()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("loading.png", width=120)

        st.markdown(
            "<h2 style='text-align: center; margin-top: 10px;'>Acceso al Sistema</h2>",
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar")

        if submit:
            if password == st.secrets["password"]:
                st.session_state["logged_in"] = True
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

# ----------------------------
# App principal
# ----------------------------
def main_app():

    inject_global_css()

    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: white !important;
            color: black !important;
        }

        :root{
            --blue-dark: #0a3d62;
            --blue-mid: #1f4e79;
            --blue-light: #eaf3fb;
        }

        .reportview-container, .main {
            background-color: var(--blue-light);
        }

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
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_title, col_logo = st.columns([6, 1])
    with col_title:
        st.title("Consulta de Responsables de Proyectos")
    with col_logo:
        st.image("loading.png", width=80)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        " 📜 Directorio Documental",
        " 🧑🏿 Responsables por Proyecto",
        " 📈 Reporte de Avances",
        " 🕰️ Horario Reuniones LP",
        " 📋 Formulario",
        " 🏢 Proyectos en grilla",
        " 📅 Cronograma de visitas",
        " ⏱️ Pull Planning"
    ])

    # ---- El resto de tus tabs permanece exactamente igual ----

# ----------------------------
# Ejecución principal
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
