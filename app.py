import streamlit as st

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(
    page_title="Sistema Corporativo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# UX GLOBAL
# ===============================
def inject_ux():
    st.markdown(
        """
        <style>
        /* =====================
           GOOGLE FONT
        ===================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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
           PALETA CORPORATIVA
        ===================== */
        :root {
            --blue-main: #1E3A5F;     /* Azul militar */
            --blue-soft: #2C5E8A;
            --bg-main: #F4F7FB;
            --card-bg: #FFFFFF;
            --text-main: #1F2933;
            --text-muted: #6B7280;
        }

        html, body, .stApp {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            font-size: 14.5px;
            letter-spacing: -0.01em;
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
            animation: fadeOut 0.35s ease forwards;
            animation-delay: 0.65s;
        }

        .loader {
            width: 44px;
            height: 44px;
            border: 4px solid #D1D9E6;
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
            padding: 2.8rem 2.6rem;
            border-radius: 20px;
            box-shadow: 0 24px 60px rgba(30,58,95,0.18);
            text-align: center;
        }

        .login-title {
            font-size: 1.45rem;
            font-weight: 600;
            color: var(--blue-main);
            margin-bottom: 1.6rem;
        }

        /* =====================
           TITULOS APP
        ===================== */
        h1, h2, h3 {
            font-weight: 600;
            letter-spacing: -0.015em;
        }

        h1 {
            font-size: 1.65rem;
            color: var(--blue-main);
        }

        /* =====================
           BOTONES
        ===================== */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, var(--blue-main), var(--blue-soft));
            color: white;
            border-radius: 10px;
            padding: 0.65rem 1.2rem;
            font-weight: 600;
            font-size: 0.95rem;
            border: none;
            transition: all 0.25s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 22px rgba(30,58,95,0.35);
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
# APP PRINCIPAL
# ===============================
def main_app():
    inject_ux()

    st.title("Consulta de Responsables de Proyectos")
    st.caption("Sistema corporativo de gestión y consulta")
    st.divider()

    tab1, tab2 = st.tabs(["📁 Directorio documental", "📊 Reportes"])

    with tab1:
        st.info("Contenido del Directorio Documental")

    with tab2:
        st.info("Dashboards y análisis")

# ===============================
# SESIÓN
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_app()
else:
    login_screen()
