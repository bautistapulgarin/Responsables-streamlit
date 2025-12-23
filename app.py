import streamlit as st
from PIL import Image

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(
    page_title="Sistema Corporativo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# UX / CSS GLOBAL
# ===============================
def inject_ux():
    st.markdown(
        """
        <style>
        /* =====================
           OCULTAR STREAMLIT
        ===================== */
        #MainMenu, footer, header,
        .stDeployButton,
        [data-testid="stToolbar"],
        [data-testid="baseButton-header"] {
            display: none !important;
        }

        /* =====================
           RESET LAYOUT
        ===================== */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
        }

        /* =====================
           PALETA CORPORATIVA
        ===================== */
        :root {
            --blue-main: #1F3A5F;   /* Azul militar */
            --blue-soft: #2F5C8F;
            --bg-main: #F2F5FA;
            --card-bg: #FFFFFF;
            --text-main: #2C2C2C;
        }

        html, body, .stApp {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        /* =====================
           LOADER
        ===================== */
        #loader-overlay {
            position: fixed;
            inset: 0;
            background: var(--bg-main);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeOut 0.4s ease forwards;
            animation-delay: 0.7s;
        }

        .loader {
            width: 46px;
            height: 46px;
            border: 4px solid #D6DEE9;
            border-top: 4px solid var(--blue-main);
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

        /* =====================
           LOGIN
        ===================== */
        .login-wrapper {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .login-card {
            background: var(--card-bg);
            width: 100%;
            max-width: 420px;
            padding: 2.6rem;
            border-radius: 18px;
            box-shadow: 0 22px 55px rgba(31,58,95,0.18);
            text-align: center;
        }

        .login-logo img {
            width: 88px;
            margin-bottom: 1rem;
        }

        .login-title {
            font-size: 1.35rem;
            font-weight: 600;
            color: var(--blue-main);
            margin-bottom: 1.8rem;
        }

        /* =====================
           BOTONES
        ===================== */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, var(--blue-main), var(--blue-soft));
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            border: none;
            transition: all 0.25s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(31,58,95,0.35);
        }
        </style>

        <div id="loader-overlay">
            <div class="loader"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ===============================
# LOGIN
# ===============================
def login_screen():
    inject_ux()

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # LOGO (coloca loading.png en la raíz del proyecto)
    try:
        st.markdown(
            '<div class="login-logo"><img src="loading.png"></div>',
            unsafe_allow_html=True
        )
    except:
        pass

    st.markdown(
        '<div class="login-title">Acceso al Sistema</div>',
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")

    if submit:
        if password == st.secrets.get("password", "admin"):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")

    st.markdown('</div></div>', unsafe_allow_html=True)

# ===============================
# APLICACIÓN PRINCIPAL
# ===============================
def main_app():
    inject_ux()

    st.title("Consulta de Responsables de Proyectos")
    st.divider()

    tab1, tab2 = st.tabs(["📁 Directorio documental", "📊 Reportes"])

    with tab1:
        st.info("Aquí va tu lógica del Directorio Documental.")

    with tab2:
        st.info("Aquí van tus dashboards, tablas y análisis.")

# ===============================
# CONTROL DE SESIÓN
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
