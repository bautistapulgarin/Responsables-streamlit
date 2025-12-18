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
    # Agregar estas opciones para ocultar elementos del menú
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ----------------------------
# Pantalla de Login
# ----------------------------
def login_screen():
    # ESTILOS ESPECÍFICOS PARA OCULTAR ELEMENTOS EN LA PANTALLA DE LOGIN
    st.markdown("""
    <style>
        /* Ocultar completamente la barra superior en la pantalla de login */
        header {
            visibility: hidden !important;
            height: 0px !important;
        }
        
        /* Ocultar el botón de deploy y menú hamburguesa */
        .stDeployButton {
            display: none !important;
        }
        
        #MainMenu {
            display: none !important;
        }
        
        footer {
            display: none !important;
        }
        
        /* Ocultar específicamente los botones de la toolbar */
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Ocultar el botón de compartir */
        [data-testid="baseButton-header"] {
            display: none !important;
        }
        
        /* Ocultar cualquier elemento con clase relacionada a header */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Ocultar el logo de Streamlit */
        [data-testid="stAppViewContainer"] > header {
            display: none !important;
        }
        
        /* Asegurar que el contenedor principal no tenga margen superior */
        .stApp {
            margin-top: -50px !important;
        }
        
        /* Estilos adicionales para el login */
        .stApp > div:first-child {
            padding-top: 0rem !important;
        }
        
        /* Ocultar cualquier elemento de acciones en header */
        .stApp > header ~ div {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("loading.png", width=120)

        st.markdown(
            "<h2 style='text-align: center; margin-top: 10px;'>Acceso al Sistema</h2>",
            unsafe_allow_html=True
        )

        # ---------- LOGIN CON FORMULARIO (AHORA ENTER FUNCIONA) ----------
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
    # Mantener los estilos existentes para la app principal
    st.markdown(
        """
    <style>
        /* Ocultar elementos del menú superior derecho */
        .stDeployButton {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden !important;
        }
        footer {
            visibility: hidden !important;
        }
        header {
            visibility: hidden !important;
        }
        
        /* Ocultar específicamente los botones de deploy */
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Ocultar el menú de hamburguesa */
        #stMainMenu {
            display: none !important;
        }
        
        /* Ocultar el botón de compartir */
        [data-testid="baseButton-header"] {
            display: none !important;
        }
        
        /* Ajustar margen superior para compensar header oculto */
        .stApp {
            margin-top: -50px !important;
        }
        
        /* Estilos existentes */
        body {
            background-color: white !important;
            color: black !important;
        }
        
        .stApp {
            background-color: white !important;
        }

        :root{
            --blue-dark: #0a3d62;
            --blue-mid: #1f4e79;
            --blue-light: #eaf3fb;
        }
        .reportview-container, .main {
            background-color: var(--blue-light);
        }
        .css-1d391kg h1, .css-1d391kg h2 {
            color: var(--blue-dark);
            font-family: "Arial", sans-serif;
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
        .stSelectbox, .stDataFrame {
            border-radius: 10px;
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

    # MODIFICACIÓN: Cambiar el orden para que "Directorio Documental" sea la primera pestaña
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        " 📜 Directorio Documental",  # AHORA ES LA PRIMERA PESTAÑA
        " 🧑🏿 Responsables por Proyecto", 
        " 📈 Reporte de Avances", 
        " 🕰️ Horario Reuniones LP",
        " 📋 Formulario",
        " 🏢 Proyectos en grilla",
        " 📅 Cronograma de visitas",
        " ⏱️ Pull Planning"
    ])
    
    # ... (el resto del código de las pestañas se mantiene igual) ...
    
    # ======================================================
    # TAB 1: Directorio Documental (AHORA ES LA PRIMERA)
    # ======================================================
    with tab1:
        st.subheader("📂 Directorio Documental")

        try:
            df_dir = pd.read_excel("data/Directorio.xlsx")
        except FileNotFoundError:
            st.error("⚠️ No se encontró el archivo 'data/Directorio.xlsx'")
            st.stop()
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            st.stop()

        columnas_esperadas = ["ID", "ID_Padre", "Nivel", "Nombre", "Tipo", "Descripción", "URL", "Orden"]
        faltantes = [c for c in columnas_esperadas if c not in df_dir.columns]
        if faltantes:
            st.error(f"El archivo no contiene las columnas requeridas: {faltantes}")
            st.stop()

        def construir_arbol(df, id_padre=None):
            df_nivel = df[df["ID_Padre"].fillna("") == (id_padre or "")]
            df_nivel = df_nivel.sort_values("Orden", ascending=True)
            arbol = []
            for _, fila in df_nivel.iterrows():
                hijos = construir_arbol(df, fila["ID"])
                arbol.append({
                    "id": fila["ID"],
                    "nombre": fila["Nombre"],
                    "tipo": str(fila["Tipo"]).strip() if pd.notna(fila["Tipo"]) else "Archivo",
                    "url": str(fila["URL"]).strip() if pd.notna(fila["URL"]) else "",
                    "descripcion": str(fila["Descripción"]).strip() if pd.notna(fila["Descripción"]) else "",
                    "hijos": hijos
                })
            return arbol

        arbol = construir_arbol(df_dir)

        def mostrar_arbol(nodos):
            for nodo in nodos:
                if nodo["tipo"].lower() == "carpeta":
                    with st.expander(f"📁 {nodo['nombre']}", expanded=False):
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

        if arbol:
            mostrar_arbol(arbol)
        else:
            st.info("No hay registros en el archivo Directorio.xlsx")

    # ... (el resto del código se mantiene igual hasta el final) ...

# ----------------------------
# Ejecución principal
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
