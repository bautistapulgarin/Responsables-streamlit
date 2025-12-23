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
# UX / UI GLOBAL
# ----------------------------
def inject_ux():
    st.markdown(
        """
        <style>
        /* ========================
           RESET STREAMLIT UI
        ======================== */
        .stDeployButton, #MainMenu, footer, header,
        [data-testid="stToolbar"],
        [data-testid="baseButton-header"] {
            display: none !important;
        }

        /* ========================
           PALETA CORPORATIVA
        ======================== */
        :root {
            --blue-main: #1F3A5F;
            --blue-soft: #2C4F7C;
            --blue-bg: #F2F6FB;
            --text-main: #2E2E2E;
            --text-soft: #8A8F98;
            --white: #FFFFFF;
        }

        /* ========================
           BASE
        ======================== */
        html, body, .stApp {
            background-color: var(--blue-bg);
            color: var(--text-main);
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        /* ========================
           LOADER OVERLAY
        ======================== */
        #loader-overlay {
            position: fixed;
            inset: 0;
            background: var(--blue-bg);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeOut 0.4s ease forwards;
            animation-delay: 0.7s;
        }

        .loader {
            width: 52px;
            height: 52px;
            border: 5px solid #D6DFEA;
            border-top: 5px solid var(--blue-main);
            border-radius: 50%;
            animation: spin 0.9s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @keyframes fadeOut {
            to {
                opacity: 0;
                visibility: hidden;
            }
        }

        /* ========================
           LOGIN CARD
        ======================== */
        .login-card {
            background: var(--white);
            padding: 2.5rem 2.5rem 2.8rem;
            border-radius: 18px;
            box-shadow: 0 18px 45px rgba(31, 58, 95, 0.18);
            text-align: center;
        }

        .login-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 0.5rem;
            color: var(--blue-main);
        }

        /* ========================
           BOTONES
        ======================== */
        .stButton>button {
            background: linear-gradient(135deg, var(--blue-main), var(--blue-soft));
            color: white;
            border-radius: 10px;
            padding: 0.55rem 1.2rem;
            font-weight: 600;
            border: none;
            transition: all 0.25s ease;
        }

        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(31, 58, 95, 0.35);
        }

        /* ========================
           INPUTS
        ======================== */
        input, textarea, select {
            border-radius: 8px !important;
        }

        /* ========================
           TÍTULOS
        ======================== */
        h1, h2, h3 {
            color: var(--blue-main);
            font-weight: 600;
        }
        </style>

        <div id="loader-overlay">
            <div class="loader"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Login
# ----------------------------
def login_screen():
    inject_ux()

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.image("loading.png", width=90)

        st.markdown(
            "<div class='login-title'>Acceso al Sistema</div>",
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar")

        if submit:
            if password == st.secrets["password"]:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# App principal
# ----------------------------
def main_app():
    inject_ux()

    col_title, col_logo = st.columns([6, 1])
    with col_title:
        st.title("Consulta de Responsables de Proyectos")
    with col_logo:
        st.image("loading.png", width=70)

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

    # 👉 TODO tu contenido actual de tabs se mantiene intacto

# ----------------------------
# Ejecución
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_app()
else:
    login_screen()
