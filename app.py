import streamlit as st 
import pandas as pd
import streamlit.components.v1 as components
import json
import io

# ============ CSS PARA OCULTAR ELEMENTOS DE STREAMLIT CLOUD/GITHUB ============
hide_streamlit_style = """
    <style>
    /* Elementos principales que debes ocultar */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Botón de deploy de Streamlit Cloud */
    [data-testid="stDeployButton"] {display: none !important;}
    
    /* Badge de "Made with Streamlit" */
    [data-testid="stAppViewContainer"] > footer {display: none !important;}
    
    /* Botones de la toolbar */
    [data-testid="stToolbar"] {display: none !important;}
    
    /* Menú de hamburguesa específico */
    button[title="View fullscreen"] {display: none !important;}
    button[title="View app source code"] {display: none !important;}
    button[title="Get app URL"] {display: none !important;}
    button[title="Share"] {display: none !important;}
    
    /* Elementos de header */
    .stApp > header {display: none !important;}
    
    /* Ajustar margen cuando se oculta header */
    .stApp {margin-top: -80px !important;}
    
    /* Ocultar cualquier elemento con clase de viewer badge */
    .viewerBadge_container__1QSob {display: none !important;}
    
    /* Elementos específicos de Streamlit Cloud */
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Ocultar el botón de menú hamburguesa */
    button[kind="header"] {display: none !important;}
    
    /* Asegurar que no haya scrollbars innecesarios */
    .stApp {overflow: hidden !important;}
    
    /* Elementos de GitHub si aparecen */
    [href*="github.com"] {display: none !important;}
    [href*="streamlit.io"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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

    # ======================================================
    # TAB 2: Responsables por Proyecto
    # ======================================================
    with tab2:
        st.subheader("🧑🏿 Responsables por Proyecto")
        
        try:
            df = pd.read_excel("ResponsablesPorProyecto.xlsx")
        except FileNotFoundError:
            st.error("⚠️ No se encontró el archivo 'ResponsablesPorProyecto.xlsx'")
            st.stop()
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            st.stop()

        # Filtrar columnas relevantes
        columnas_relevantes = [col for col in df.columns if "Unnamed" not in col]
        df = df[columnas_relevantes]

        # Mostrar filtro por proyecto si existe la columna
        if "Proyecto" in df.columns:
            proyectos = ["Todos"] + sorted(df["Proyecto"].dropna().unique().tolist())
            proyecto_seleccionado = st.selectbox("Seleccionar Proyecto", proyectos)
            
            if proyecto_seleccionado != "Todos":
                df = df[df["Proyecto"] == proyecto_seleccionado]

        # Mostrar filtro por responsable si existe la columna
        if "Responsable" in df.columns:
            responsables = ["Todos"] + sorted(df["Responsable"].dropna().unique().tolist())
            responsable_seleccionado = st.selectbox("Seleccionar Responsable", responsables)
            
            if responsable_seleccionado != "Todos":
                df = df[df["Responsable"] == responsable_seleccionado]

        # Mostrar datos
        st.dataframe(df, use_container_width=True)
        
        # Opción para descargar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar como CSV",
            data=csv,
            file_name="responsables_proyecto.csv",
            mime="text/csv",
        )

    # ======================================================
    # TAB 3: Reporte de Avances
    # ======================================================
    with tab3:
        st.subheader("📈 Reporte de Avances")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Proyectos Activos", "24", "3")
            st.metric("Tareas Completadas", "156", "12")
        
        with col2:
            st.metric("Proyectos Atrasados", "5", "-2")
            st.metric("Porcentaje de Avance", "78%", "5%")
        
        st.markdown("---")
        
        # Datos de ejemplo para gráficos
        data = {
            'Proyecto': ['Proyecto A', 'Proyecto B', 'Proyecto C', 'Proyecto D', 'Proyecto E'],
            'Avance': [85, 60, 90, 45, 75],
            'Presupuesto Utilizado': [78, 65, 82, 50, 70]
        }
        df_avances = pd.DataFrame(data)
        
        st.bar_chart(df_avances.set_index('Proyecto'))
        
        st.markdown("### 📋 Detalle por Proyecto")
        st.dataframe(df_avances)

    # ======================================================
    # TAB 4: Horario Reuniones LP
    # ======================================================
    with tab4:
        st.subheader("🕰️ Horario Reuniones LP")
        
        # Datos de ejemplo para horarios
        reuniones_data = {
            'Día': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
            'Hora': ['9:00 AM', '10:30 AM', '2:00 PM', '11:00 AM', '4:00 PM'],
            'Tipo': ['Seguimiento', 'Planificación', 'Revisión', 'Coordinación', 'Cierre'],
            'Responsable': ['Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez', 'Pedro Rodríguez'],
            'Proyecto': ['LP-001', 'LP-002', 'LP-003', 'LP-004', 'LP-005']
        }
        df_reuniones = pd.DataFrame(reuniones_data)
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            dia_filtro = st.selectbox("Filtrar por día", ["Todos"] + reuniones_data['Día'])
        
        with col2:
            responsable_filtro = st.selectbox("Filtrar por responsable", ["Todos"] + reuniones_data['Responsable'])
        
        # Aplicar filtros
        df_filtrado = df_reuniones.copy()
        if dia_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Día'] == dia_filtro]
        if responsable_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Responsable'] == responsable_filtro]
        
        # Mostrar tabla
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Calendario simple
        st.markdown("### 📅 Calendario Semanal")
        calendario_html = """
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #0a3d62; color: white;">
                <th style="padding: 10px; text-align: center;">Día</th>
                <th style="padding: 10px; text-align: center;">Reuniones</th>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">Lunes</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Seguimiento LP-001 (9:00 AM)</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">Martes</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Planificación LP-002 (10:30 AM)</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">Miércoles</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Revisión LP-003 (2:00 PM)</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">Jueves</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Coordinación LP-004 (11:00 AM)</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">Viernes</td>
                <td style="padding: 10px; border: 1px solid #ddd;">Cierre LP-005 (4:00 PM)</td>
            </tr>
        </table>
        </div>
        """
        st.markdown(calendario_html, unsafe_allow_html=True)

    # ======================================================
    # TAB 5: Formulario
    # ======================================================
    with tab5:
        st.subheader("📋 Formulario de Registro")
        
        with st.form("formulario_registro"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre Completo")
                proyecto = st.text_input("Proyecto Asignado")
                fecha_inicio = st.date_input("Fecha de Inicio")
            
            with col2:
                email = st.text_input("Correo Electrónico")
                telefono = st.text_input("Teléfono")
                fecha_fin = st.date_input("Fecha Estimada de Fin")
            
            rol = st.selectbox("Rol en el Proyecto", 
                              ["Gerente", "Coordinador", "Supervisor", "Técnico", "Consultor"])
            
            descripcion = st.text_area("Descripción de Actividades")
            
            archivo = st.file_uploader("Subir Documento Relacionado", type=['pdf', 'docx', 'xlsx'])
            
            submitted = st.form_submit_button("Guardar Registro")
            
            if submitted:
                if nombre and proyecto and email:
                    st.success("✅ Registro guardado exitosamente")
                    
                    # Crear registro en DataFrame
                    registro = {
                        'Nombre': nombre,
                        'Email': email,
                        'Teléfono': telefono,
                        'Proyecto': proyecto,
                        'Rol': rol,
                        'Fecha Inicio': fecha_inicio,
                        'Fecha Fin': fecha_fin,
                        'Descripción': descripcion
                    }
                    
                    # Mostrar resumen
                    st.markdown("### 📄 Resumen del Registro")
                    st.json(registro)
                else:
                    st.error("⚠️ Por favor complete los campos obligatorios (Nombre, Proyecto, Email)")

    # ======================================================
    # TAB 6: Proyectos en grilla
    # ======================================================
    with tab6:
        st.subheader("🏢 Proyectos en Grilla")
        
        # Datos de ejemplo
        proyectos_data = {
            'ID': ['P-001', 'P-002', 'P-003', 'P-004', 'P-005'],
            'Nombre': ['Edificio Torres', 'Centro Comercial', 'Hospital Regional', 'Conjunto Residencial', 'Planta Industrial'],
            'Estado': ['En Progreso', 'Completado', 'En Progreso', 'Planificado', 'En Pausa'],
            'Ubicación': ['Zona Norte', 'Zona Centro', 'Zona Sur', 'Zona Este', 'Zona Oeste'],
            'Presupuesto (M)': [50, 120, 200, 85, 150],
            'Avance': [65, 100, 45, 0, 30]
        }
        df_proyectos = pd.DataFrame(proyectos_data)
        
        # Mostrar en formato de tarjetas
        cols = st.columns(3)
        for idx, row in df_proyectos.iterrows():
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #eaf3fb; padding: 15px; border-radius: 10px; border-left: 5px solid #0a3d62; margin-bottom: 10px;">
                        <h4>{row['Nombre']}</h4>
                        <p><strong>ID:</strong> {row['ID']}</p>
                        <p><strong>Estado:</strong> {row['Estado']}</p>
                        <p><strong>Ubicación:</strong> {row['Ubicación']}</p>
                        <p><strong>Presupuesto:</strong> ${row['Presupuesto (M)']}M</p>
                        <p><strong>Avance:</strong> {row['Avance']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📊 Vista Detallada")
        st.dataframe(df_proyectos, use_container_width=True)

    # ======================================================
    # TAB 7: Cronograma de visitas
    # ======================================================
    with tab7:
        st.subheader("📅 Cronograma de Visitas")
        
        # Datos de ejemplo
        visitas_data = {
            'Fecha': ['2024-01-15', '2024-01-18', '2024-01-22', '2024-01-25', '2024-01-30'],
            'Hora': ['9:00 AM', '2:00 PM', '10:00 AM', '11:00 AM', '3:00 PM'],
            'Proyecto': ['Edificio Torres', 'Centro Comercial', 'Hospital Regional', 'Conjunto Residencial', 'Planta Industrial'],
            'Tipo Visita': ['Supervisión', 'Inspección', 'Revisión', 'Coordinación', 'Entrega'],
            'Responsable': ['Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez', 'Pedro Rodríguez'],
            'Estado': ['Programada', 'Realizada', 'Programada', 'Cancelada', 'Programada']
        }
        df_visitas = pd.DataFrame(visitas_data)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            estado_filtro = st.selectbox("Filtrar por estado", ["Todos"] + list(df_visitas['Estado'].unique()))
        
        with col2:
            proyecto_filtro = st.selectbox("Filtrar por proyecto", ["Todos"] + list(df_visitas['Proyecto'].unique()))
        
        with col3:
            fecha_inicio = st.date_input("Fecha desde")
        
        # Aplicar filtros
        df_filtrado_visitas = df_visitas.copy()
        if estado_filtro != "Todos":
            df_filtrado_visitas = df_filtrado_visitas[df_filtrado_visitas['Estado'] == estado_filtro]
        if proyecto_filtro != "Todos":
            df_filtrado_visitas = df_filtrado_visitas[df_filtrado_visitas['Proyecto'] == proyecto_filtro]
        
        # Mostrar tabla
        st.dataframe(df_filtrado_visitas, use_container_width=True)
        
        # Estadísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Visitas Programadas", 
                     len(df_visitas[df_visitas['Estado'] == 'Programada']))
        with col2:
            st.metric("Visitas Realizadas", 
                     len(df_visitas[df_visitas['Estado'] == 'Realizada']))
        with col3:
            st.metric("Visitas Canceladas", 
                     len(df_visitas[df_visitas['Estado'] == 'Cancelada']))

    # ======================================================
    # TAB 8: Pull Planning
    # ======================================================
    with tab8:
        st.subheader("⏱️ Pull Planning")
        
        # Datos de ejemplo para Pull Planning
        planning_data = {
            'Actividad': ['Cimentación', 'Estructura', 'Instalaciones', 'Acabados', 'Paisajismo'],
            'Responsable': ['Carlos López', 'Juan Pérez', 'María García', 'Ana Martínez', 'Pedro Rodríguez'],
            'Inicio': ['2024-01-10', '2024-02-01', '2024-03-15', '2024-04-10', '2024-05-01'],
            'Fin': ['2024-01-31', '2024-03-14', '2024-04-09', '2024-04-30', '2024-05-20'],
            'Duración (días)': [21, 42, 25, 20, 19],
            'Estado': ['Completado', 'En Progreso', 'Planificado', 'Planificado', 'Planificado']
        }
        df_planning = pd.DataFrame(planning_data)
        
        # Mostrar diagrama de Gantt simple
        st.markdown("### 📊 Diagrama de Actividades")
        
        # Crear representación visual simple
        for idx, row in df_planning.iterrows():
            col1, col2 = st.columns([3, 7])
            with col1:
                st.write(f"**{row['Actividad']}**")
                st.caption(f"Responsable: {row['Responsable']}")
            with col2:
                estado_color = {
                    'Completado': '#4CAF50',
                    'En Progreso': '#2196F3',
                    'Planificado': '#FF9800'
                }
                color = estado_color.get(row['Estado'], '#9E9E9E')
                progress = 100 if row['Estado'] == 'Completado' else (50 if row['Estado'] == 'En Progreso' else 0)
                st.progress(progress/100, text=f"{row['Estado']} - {row['Duración (días)']} días")
        
        st.markdown("---")
        st.markdown("### 📋 Detalle del Plan")
        st.dataframe(df_planning, use_container_width=True)
        
        # Opciones de filtro
        col1, col2 = st.columns(2)
        with col1:
            estado_planning = st.selectbox("Estado de actividades", 
                                         ["Todos", "Completado", "En Progreso", "Planificado"])
        
        if estado_planning != "Todos":
            df_filtrado_planning = df_planning[df_planning['Estado'] == estado_planning]
            st.metric(f"Actividades {estado_planning.lower()}", len(df_filtrado_planning))

# ----------------------------
# Ejecución principal
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
    
