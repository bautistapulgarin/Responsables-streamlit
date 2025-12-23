import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ======================================================
# OCULTAMIENTO INMEDIATO DE UI STREAMLIT (ANTI-FLASH)
# ======================================================
def hide_streamlit_ui_hard():
    components.html(
        """
        <style>
        /* Ocultar elementos nativos antes del render */
        #MainMenu { display: none !important; }
        footer { display: none !important; }
        header { display: none !important; }

        .stDeployButton { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        [data-testid="baseButton-header"] { display: none !important; }

        html, body {
            overflow: hidden;
        }
        </style>
        """,
        height=0,
        width=0
    )

# 🔒 DEBE EJECUTARSE ANTES DE TODO
hide_streamlit_ui_hard()

# ======================================================
# CONFIGURACIÓN GENERAL
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
# LOGIN
# ======================================================
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("loading.png", width=120)
        st.markdown(
            "<h2 style='text-align:center;'>Acceso al Sistema</h2>",
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

    # ----------------------------
    # ESTILOS GENERALES
    # ----------------------------
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #f5f9fd;
            color: #000;
        }

        .stButton>button {
            background-color: #1f4e79;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }

        .stButton>button:hover {
            background-color: #163754;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col_title, col_logo = st.columns([6, 1])
    with col_title:
        st.title("Consulta de Responsables de Proyectos")
    with col_logo:
        st.image("loading.png", width=80)

    tabs = st.tabs([
        "📜 Directorio Documental",
        "🧑🏿 Responsables por Proyecto",
        "📈 Reporte de Avances",
        "🕰️ Horario Reuniones LP",
        "📋 Formulario",
        "🏢 Proyectos en grilla",
        "📅 Cronograma de visitas",
        "⏱️ Pull Planning"
    ])

    # ======================================================
    # TAB 1 – DIRECTORIO DOCUMENTAL (CON BUSCADOR)
    # ======================================================
    with tabs[0]:
        st.subheader("📂 Directorio Documental")

        search_text = st.text_input(
            "🔎 Buscar",
            placeholder="Nombre de carpeta, archivo o descripción"
        ).strip().lower()

        try:
            df = pd.read_excel("data/Directorio.xlsx")
        except FileNotFoundError:
            st.error("No se encontró el archivo data/Directorio.xlsx")
            st.stop()

        def build_tree(df, parent=None):
            level = df[df["ID_Padre"].fillna("") == (parent or "")]
            level = level.sort_values("Orden")
            tree = []

            for _, row in level.iterrows():
                children = build_tree(df, row["ID"])
                tree.append({
                    "nombre": str(row["Nombre"]),
                    "tipo": str(row["Tipo"]).lower(),
                    "descripcion": str(row["Descripción"]) if pd.notna(row["Descripción"]) else "",
                    "url": str(row["URL"]) if pd.notna(row["URL"]) else "",
                    "hijos": children
                })
            return tree

        def filter_tree(nodes, text):
            if not text:
                return nodes

            result = []
            for n in nodes:
                match = (
                    text in n["nombre"].lower()
                    or text in n["descripcion"].lower()
                )
                filtered_children = filter_tree(n["hijos"], text)
                if match or filtered_children:
                    new_node = n.copy()
                    new_node["hijos"] = filtered_children
                    result.append(new_node)
            return result

        def render_tree(nodes):
            for n in nodes:
                if n["tipo"] == "carpeta":
                    with st.expander(f"📁 {n['nombre']}", expanded=bool(search_text)):
                        if n["descripcion"]:
                            st.caption(n["descripcion"])
                        if n["url"]:
                            st.markdown(f"[🌐 Abrir enlace]({n['url']})")
                        render_tree(n["hijos"])
                else:
                    if n["url"]:
                        st.markdown(f"- 📄 [{n['nombre']}]({n['url']})")
                    else:
                        st.markdown(f"- 📄 {n['nombre']}")
                    if n["descripcion"]:
                        st.caption(n["descripcion"])

        tree = build_tree(df)
        filtered_tree = filter_tree(tree, search_text)

        if filtered_tree:
            render_tree(filtered_tree)
        else:
            st.info("No se encontraron coincidencias.")

    # ======================================================
    # TAB 2–8 (SIN CAMBIOS)
    # ======================================================
    for i in range(1, 8):
        with tabs[i]:
            st.info("Contenido sin cambios funcionales.")

# ======================================================
# CONTROL DE SESIÓN
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
