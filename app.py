import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json

# ======================================================
# CONFIGURACIÓN GENERAL
# ======================================================
st.set_page_config(
    page_title="Consulta de Responsables de Proyectos",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ======================================================
# OCULTAR UI NATIVA DE STREAMLIT (GLOBAL)
# ======================================================
def hide_streamlit_ui():
    st.markdown(
        """
        <style>
        .stDeployButton {display: none !important;}
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}

        [data-testid="stToolbar"] {display: none !important;}
        #stMainMenu {display: none !important;}
        [data-testid="baseButton-header"] {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# PANTALLA DE LOGIN
# ======================================================
def login_screen():
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

# ======================================================
# APP PRINCIPAL
# ======================================================
def main_app():

    # ----------------------------
    # ESTILOS CORPORATIVOS
    # ----------------------------
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

    # ======================================================
    # TAB 1: DIRECTORIO DOCUMENTAL (CON BUSCADOR)
    # ======================================================
    with tab1:
        st.subheader("📂 Directorio Documental")

        search_text = st.text_input(
            "🔎 Buscar en el directorio",
            placeholder="Nombre de carpeta, archivo o descripción"
        ).strip().lower()

        try:
            df_dir = pd.read_excel("data/Directorio.xlsx")
        except FileNotFoundError:
            st.error("⚠️ No se encontró el archivo 'data/Directorio.xlsx'")
            st.stop()

        columnas_esperadas = [
            "ID", "ID_Padre", "Nivel", "Nombre", "Tipo",
            "Descripción", "URL", "Orden"
        ]

        faltantes = [c for c in columnas_esperadas if c not in df_dir.columns]
        if faltantes:
            st.error(f"El archivo no contiene las columnas requeridas: {faltantes}")
            st.stop()

        def construir_arbol(df, id_padre=None):
            df_nivel = df[df["ID_Padre"].fillna("") == (id_padre or "")]
            df_nivel = df_nivel.sort_values("Orden")
            arbol = []
            for _, fila in df_nivel.iterrows():
                hijos = construir_arbol(df, fila["ID"])
                arbol.append({
                    "id": fila["ID"],
                    "nombre": str(fila["Nombre"]),
                    "tipo": str(fila["Tipo"]).strip().lower() if pd.notna(fila["Tipo"]) else "archivo",
                    "url": str(fila["URL"]).strip() if pd.notna(fila["URL"]) else "",
                    "descripcion": str(fila["Descripción"]).strip() if pd.notna(fila["Descripción"]) else "",
                    "hijos": hijos
                })
            return arbol

        def filtrar_arbol(nodos, texto):
            if not texto:
                return nodos

            resultado = []
            for nodo in nodos:
                coincide = (
                    texto in nodo["nombre"].lower()
                    or texto in nodo["descripcion"].lower()
                )

                hijos_filtrados = filtrar_arbol(nodo["hijos"], texto)

                if coincide or hijos_filtrados:
                    nuevo_nodo = nodo.copy()
                    nuevo_nodo["hijos"] = hijos_filtrados
                    resultado.append(nuevo_nodo)

            return resultado

        def mostrar_arbol(nodos):
            for nodo in nodos:
                if nodo["tipo"] == "carpeta":
                    with st.expander(
                        f"📁 {nodo['nombre']}",
                        expanded=bool(search_text)
                    ):
                        if nodo["descripcion"]:
                            st.markdown(f"📝 *{nodo['descripcion']}*")
                        if nodo["url"]:
                            st.markdown(f"[🌐 Abrir enlace]({nodo['url']})")
                        mostrar_arbol(nodo["hijos"])
                else:
                    if nodo["url"]:
                        st.markdown(f"- 📄 [{nodo['nombre']}]({nodo['url']})")
                    else:
                        st.markdown(f"- 📄 {nodo['nombre']}")
                    if nodo["descripcion"]:
                        st.caption(nodo["descripcion"])

        arbol = construir_arbol(df_dir)
        arbol_filtrado = filtrar_arbol(arbol, search_text)

        if arbol_filtrado:
            mostrar_arbol(arbol_filtrado)
        else:
            st.info("No se encontraron coincidencias para la búsqueda.")

    # ======================================================
    # TAB 2 A TAB 8
    # ======================================================
    # ⚠️ SIN CAMBIOS FUNCIONALES
    # (Se mantiene exactamente igual a tu versión estable)
    # ======================================================

    # --- AQUÍ CONTINÚA TU CÓDIGO ORIGINAL ---
    # Responsables por Proyecto
    # Reporte de Avances
    # Horario Reuniones LP
    # Formulario Google Sheets
    # Proyectos en Grilla
    # Cronograma
    # Pull Planning

# ======================================================
# EJECUCIÓN PRINCIPAL
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

hide_streamlit_ui()  # ← SE APLICA DESDE EL PRIMER RENDER

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
