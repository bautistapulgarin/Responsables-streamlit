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

    st.markdown(
        """
    <style>
        /* Ocultar elementos del menú superior derecho */
        .stDeployButton {
            display: none;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        header {
            visibility: hidden;
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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        " 🧑🏿 Responsables por Proyecto", 
        " 📈 Reporte de Avances", 
        " 🕰️ Horario Reuniones LP",
        " 📜 Directorio Documental",
        " 📋 Formulario",
        " 🏢 Proyectos en grilla",
        " 📅 Cronograma de visitas",
        " ⏱️ Pull Planning"
    ])
    
    # ======================================================
    # TAB 1: Responsables
    # ======================================================
    with tab1:
        def load_data():
            return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

        df = load_data()

        for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado", "gerente", "responsable_texto"]:
            if filtro not in st.session_state:
                st.session_state[filtro] = [] if filtro != "responsable_texto" else ""

        st.markdown("---")
        if st.button("Restablecer filtros"):
            for filtro in ["sucursal", "cluster", "proyecto", "cargo", "estado", "gerente"]:
                st.session_state[filtro] = []
            st.session_state["responsable_texto"] = ""

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            sucursal = st.multiselect("Sucursal", sorted(df["Sucursal"].dropna().unique().tolist()), key="sucursal")
        with col2:
            cluster = st.multiselect("Cluster", sorted(df["Cluster"].dropna().unique().tolist()), key="cluster")
        with col3:
            proyecto = st.multiselect("Proyecto", sorted(df["Proyecto"].dropna().unique().tolist()), key="proyecto")
        with col4:
            cargo = st.multiselect("Cargo", sorted(df["Cargo"].dropna().unique().tolist()), key="cargo")
        with col5:
            estado = st.multiselect("Estado", sorted(df["Estado"].dropna().unique().tolist()), key="estado")
        with col6:
            gerentes_unicos = df.loc[df["Cargo"] == "Gerente de proyectos", "Responsable"].dropna().unique().tolist()
            gerente = st.multiselect("Gerente de proyectos", sorted(gerentes_unicos), key="gerente")

        responsable_texto = st.text_input("🔎 Buscar por responsable (texto libre)", key="responsable_texto")

        df_filtrado = df.copy()

        if gerente:
            proyectos_del_gerente = df.loc[
                (df["Cargo"] == "Gerente de proyectos") & (df["Responsable"].isin(gerente)),
                "Proyecto"
            ].unique().tolist()
            df_filtrado = df[df["Proyecto"].isin(proyectos_del_gerente)]
        else:
            if sucursal:
                df_filtrado = df_filtrado[df_filtrado["Sucursal"].isin(sucursal)]
            if cluster:
                df_filtrado = df_filtrado[df_filtrado["Cluster"].isin(cluster)]
            if proyecto:
                df_filtrado = df_filtrado[df_filtrado["Proyecto"].isin(proyecto)]
            if cargo:
                df_filtrado = df_filtrado[df_filtrado["Cargo"].isin(cargo)]
            if estado:
                df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]

        if responsable_texto.strip():
            df_filtrado = df_filtrado[
                df_filtrado["Responsable"].str.contains(responsable_texto, case=False, na=False)
            ]

        st.markdown("---")
        st.subheader("Resultados de la consulta")

        if not df_filtrado.empty:
            st.dataframe(
                df_filtrado[
                    ["Sucursal", "Cluster", "Proyecto", "HC", "Cargo", "Responsable",
                     "FechaIngreso", "Estado", "Correo", "Celular"]
                ],
                use_container_width=True,
            )

            correos = df_filtrado["Correo"].dropna().tolist()
            correos_str = "\n".join(correos)

            if correos_str.strip():
                correos_json = json.dumps(correos_str)
                html = f"""
                <div style="font-family: Arial, sans-serif; margin-top:15px;">
                  <button id="copy-btn" style="
                      padding:10px 16px;
                      font-size:14px;
                      background-color:#1f4e79;
                      color:#ffffff;
                      border:none;
                      border-radius:8px;
                      font-weight:600;
                      cursor:pointer;
                  ">Copiar correos</button>
                  <div id="msg" style="height:18px; font-size:13px; color:#0a3d62; margin-top:6px;"></div>

                  <script>
                    const text = {correos_json};
                    const copyBtn = document.getElementById("copy-btn");
                    const msg = document.getElementById("msg");

                    copyBtn.addEventListener("click", async () => {{
                      try {{
                        await navigator.clipboard.writeText(text);
                        msg.innerText = "Copiado";
                      }} catch (e) {{
                        try {{
                          const ta = document.createElement("textarea");
                          ta.value = text;
                          document.body.appendChild(ta);
                          ta.select();
                          document.execCommand('copy');
                          document.body.removeChild(ta);
                          msg.innerText = "Copiado (fallback)";
                        }} catch (ee) {{
                          msg.innerText = "No fue posible copiar automáticamente. Use Ctrl+C.";
                        }}
                      }}
                      setTimeout(()=>msg.innerText = "", 2500);
                    }});
                  </script>
                </div>
                """
                components.html(html, height=100)
            else:
                st.write("No hay correos para copiar.")
        else:
            st.warning("No se encontraron resultados con los filtros seleccionados.")

    # ======================================================
    # TAB 2
    # ======================================================
    with tab2:
        st.subheader("📈 Reporte de Avances")
        try:
            df_avances = pd.read_excel("data/ReporteAvances.xlsx")
            st.dataframe(df_avances, use_container_width=True)
        except FileNotFoundError:
            st.error("No se encontró el archivo 'data/ReporteAvances.xlsx'")
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    # ======================================================
    # TAB 3
    # ======================================================
    with tab3:
        st.subheader("🕒 Horario Reuniones LP")
        st.info("Esta sección está en construcción.")

        try:
            df_horario = pd.read_excel("data/HorarioReuniones.xlsx")
            st.dataframe(df_horario, use_container_width=True)
        except FileNotFoundError:
            st.error("⚠️ No se encontró el archivo 'data/HorarioReuniones.xlsx'")
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    # ======================================================
    # TAB 4
    # ======================================================
    with tab4:
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
    # TAB 5
    # ======================================================
    with tab5:
        st.subheader("📋 Formulario de Registro")
        st.info("Completa el siguiente formulario para registrar la información en Google Sheets.")

        import gspread
        from google.oauth2.service_account import Credentials
        from datetime import datetime

        creds_info = st.secrets["google_service_account"]
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        client = gspread.authorize(creds)
        SHEET_ID = "1PvlOcqy-B7uOcPeKvaGO18cssIEnb6UIXeNBRuVQpiE"
        sheet = client.open_by_key(SHEET_ID).sheet1

        with st.form("registro_form"):
            nombre = st.text_input("👤 Nombre completo")
            categoria = st.selectbox("📂 Categoría", ["Avance", "Reunión", "Observación", "Otro"])
            comentario = st.text_area("💬 Comentario")
            submitted = st.form_submit_button("✅ Enviar")

            if submitted:
                if nombre and comentario:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sheet.append_row([timestamp, nombre, categoria, comentario])
                    st.success("Registro enviado correctamente ✅")
                else:
                    st.warning("Por favor completa al menos el nombre y el comentario.")


    # ======================================================
    # TAB 6
    # ======================================================
    # ======================================================
    # TAB 6
    # ======================================================
    with tab6:
        st.subheader("🏢 Proyectos en grilla")
        st.info("Se refleja el estado de activación de la funcionalidad de grilla")
        
        try:
            # Cargar el archivo EstadoGrilla desde GitHub
            df_grilla = pd.read_excel("data/EstadoGrilla.xlsx")
            
            # --- FILTROS PARA LA TABLA PRINCIPAL ---
            st.markdown("### Filtros")
            
            # Inicializar estados de sesión para los filtros si no existen
            if "filtro_proyecto" not in st.session_state:
                st.session_state.filtro_proyecto = []
            if "filtro_estado_grilla" not in st.session_state:
                st.session_state.filtro_estado_grilla = []
            if "filtro_prioridad" not in st.session_state:
                st.session_state.filtro_prioridad = []
            if "filtro_componente" not in st.session_state:
                st.session_state.filtro_componente = []
            if "filtro_alistamiento" not in st.session_state:  # NUEVO: filtro para Alistamiento
                st.session_state.filtro_alistamiento = []
            
            # Control único para el reset
            if "reset_counter" not in st.session_state:
                st.session_state.reset_counter = 0
            
            # Botón para restablecer filtros - SOLUCIÓN DEFINITIVA
            if st.button("🔄 Restablecer filtros", key="reset_filtros_grilla"):
                st.session_state.filtro_proyecto = []
                st.session_state.filtro_estado_grilla = []
                st.session_state.filtro_prioridad = []
                st.session_state.filtro_componente = []
                st.session_state.filtro_alistamiento = []  # NUEVO: reset del filtro Alistamiento
                st.session_state.reset_counter += 1
                st.success("Filtros restablecidos correctamente")
                st.rerun()
            
            # Identificar la columna de estado
            estado_col = None
            posibles_nombres_estado = ['Estado', 'Estado grilla', 'EstadoGrilla', 'Estado_grilla', 'Estado Grilla', 'EstadoGrila']
            for nombre in posibles_nombres_estado:
                if nombre in df_grilla.columns:
                    estado_col = nombre
                    break
            
            # PRIMER FILTRO: Estado grilla
            col1, col2 = st.columns(2)
            
            with col1:
                # Filtro por Estado grilla (PRIMERO) - CON CLAVE ÚNICA PARA RESET
                if estado_col:
                    opciones_estado = sorted(df_grilla[estado_col].dropna().unique().tolist())
                    filtro_estado_grilla = st.multiselect(
                        "📊 Estado grilla",
                        options=opciones_estado,
                        default=st.session_state.filtro_estado_grilla,
                        key=f"estado_grilla_{st.session_state.reset_counter}"
                    )
                    st.session_state.filtro_estado_grilla = filtro_estado_grilla
                else:
                    st.info("No hay columna de estado disponible")
            
            with col2:
                # NUEVO FILTRO: Alistamiento - CON CLAVE ÚNICA PARA RESET
                # Identificar la columna de Alistamiento
                alistamiento_col = None
                posibles_nombres_alistamiento = ['Alistamiento', 'Alist', 'AlistamientoGrilla', 'Alistamiento_grilla', 'Alistamiento Grilla']
                
                for nombre in posibles_nombres_alistamiento:
                    if nombre in df_grilla.columns:
                        alistamiento_col = nombre
                        break
                
                if alistamiento_col:
                    opciones_alistamiento = sorted(df_grilla[alistamiento_col].dropna().unique().tolist())
                    filtro_alistamiento = st.multiselect(
                        "🛠️ Alistamiento",  # NUEVO: icono y etiqueta
                        options=opciones_alistamiento,
                        default=st.session_state.filtro_alistamiento,
                        key=f"alistamiento_{st.session_state.reset_counter}"  # Clave única que cambia con cada reset
                    )
                    st.session_state.filtro_alistamiento = filtro_alistamiento
                else:
                    st.info("No hay columna 'Alistamiento' disponible")
            
            # Crear DataFrame base para filtros dependientes
            df_filtrado_base = df_grilla.copy()
            
            # Aplicar filtro de estado al DataFrame base para los otros filtros
            if st.session_state.filtro_estado_grilla and estado_col:
                df_filtrado_base = df_filtrado_base[df_filtrado_base[estado_col].isin(st.session_state.filtro_estado_grilla)]
            
            # Aplicar filtro de alistamiento al DataFrame base para los otros filtros
            if st.session_state.filtro_alistamiento and alistamiento_col:
                df_filtrado_base = df_filtrado_base[df_filtrado_base[alistamiento_col].isin(st.session_state.filtro_alistamiento)]
            
            # SEGUNDO FILTRO: Proyecto (dependiente del estado y alistamiento)
            col3, col4 = st.columns(2)
            
            with col3:
                if 'Proyecto' in df_filtrado_base.columns:
                    # Las opciones de proyecto se basan en el DataFrame ya filtrado por estado y alistamiento
                    opciones_proyecto = sorted(df_filtrado_base['Proyecto'].dropna().unique().tolist())
                    filtro_proyecto = st.multiselect(
                        "📋 Proyecto",
                        options=opciones_proyecto,
                        default=st.session_state.filtro_proyecto,
                        key=f"proyecto_{st.session_state.reset_counter}"
                    )
                    st.session_state.filtro_proyecto = filtro_proyecto
                else:
                    st.info("No hay columna 'Proyecto' disponible")
            
            # Aplicar filtro de proyecto al DataFrame base para prioridad y componente
            if st.session_state.filtro_proyecto and 'Proyecto' in df_filtrado_base.columns:
                df_filtrado_base = df_filtrado_base[df_filtrado_base['Proyecto'].isin(st.session_state.filtro_proyecto)]
            
            # TERCER FILTRO: Prioridad (dependiente de estado, alistamiento y proyecto)
            col5, col6 = st.columns(2)
            
            with col5:
                # Filtro por Prioridad
                if 'Prioridad' in df_filtrado_base.columns:
                    opciones_prioridad = sorted(df_filtrado_base['Prioridad'].dropna().unique().tolist())
                    filtro_prioridad = st.multiselect(
                        "🎯 Prioridad",
                        options=opciones_prioridad,
                        default=st.session_state.filtro_prioridad,
                        key=f"prioridad_{st.session_state.reset_counter}"
                    )
                    st.session_state.filtro_prioridad = filtro_prioridad
                else:
                    st.info("No hay columna 'Prioridad' disponible")
            
            with col6:
                # CUARTO FILTRO: Componente (dependiente de estado, alistamiento, proyecto y prioridad)
                # Identificar la columna de componente
                componente_col = None
                posibles_nombres_componente = ['Componente', 'Component', 'ComponenteGrilla', 'Componente_grilla', 'Componente Grilla']
                
                for nombre in posibles_nombres_componente:
                    if nombre in df_filtrado_base.columns:
                        componente_col = nombre
                        break
                
                if componente_col:
                    # Aplicar filtros anteriores al DataFrame para las opciones de componente
                    df_para_componente = df_filtrado_base.copy()
                    
                    # Aplicar filtro de prioridad si existe
                    if st.session_state.filtro_prioridad and 'Prioridad' in df_para_componente.columns:
                        df_para_componente = df_para_componente[df_para_componente['Prioridad'].isin(st.session_state.filtro_prioridad)]
                    
                    opciones_componente = sorted(df_para_componente[componente_col].dropna().unique().tolist())
                    filtro_componente = st.multiselect(
                        "⚙️ Componente",
                        options=opciones_componente,
                        default=st.session_state.filtro_componente,
                        key=f"componente_{st.session_state.reset_counter}"
                    )
                    st.session_state.filtro_componente = filtro_componente
                else:
                    st.info("No hay columna 'Componente' disponible")
            
            # Mostrar estado actual de los filtros
            st.markdown("---")
            filtros_activos = False
            info_text = "🔍 **Estado de filtros:**\n\n"
            
            if st.session_state.filtro_estado_grilla:
                info_text += f"• 📊 **Estado grilla:** {', '.join(st.session_state.filtro_estado_grilla)}\n"
                filtros_activos = True
            else:
                info_text += "• 📊 **Estado grilla:** Sin filtro\n"
            
            # NUEVO: Mostrar estado del filtro Alistamiento
            if st.session_state.filtro_alistamiento:
                info_text += f"• 🛠️ **Alistamiento:** {', '.join(st.session_state.filtro_alistamiento)}\n"
                filtros_activos = True
            else:
                info_text += "• 🛠️ **Alistamiento:** Sin filtro\n"
            
            if st.session_state.filtro_proyecto:
                info_text += f"• 📋 **Proyectos:** {len(st.session_state.filtro_proyecto)} seleccionados\n"
                filtros_activos = True
            else:
                info_text += "• 📋 **Proyectos:** Sin filtro\n"
            
            if st.session_state.filtro_prioridad:
                info_text += f"• 🎯 **Prioridad:** {', '.join(st.session_state.filtro_prioridad)}\n"
                filtros_activos = True
            else:
                info_text += "• 🎯 **Prioridad:** Sin filtro\n"
            
            if st.session_state.filtro_componente:
                info_text += f"• ⚙️ **Componente:** {', '.join(st.session_state.filtro_componente)}\n"
                filtros_activos = True
            else:
                info_text += "• ⚙️ **Componente:** Sin filtro\n"
            
            if filtros_activos:
                st.success(info_text)
            else:
                st.info(info_text)
            
            # APLICAR TODOS LOS FILTROS AL DATAFRAME FINAL
            df_filtrado_final = df_grilla.copy()
            
            # Aplicar filtro de Estado grilla
            if st.session_state.filtro_estado_grilla and estado_col:
                df_filtrado_final = df_filtrado_final[df_filtrado_final[estado_col].isin(st.session_state.filtro_estado_grilla)]
            
            # NUEVO: Aplicar filtro de Alistamiento
            if st.session_state.filtro_alistamiento and alistamiento_col:
                df_filtrado_final = df_filtrado_final[df_filtrado_final[alistamiento_col].isin(st.session_state.filtro_alistamiento)]
            
            # Aplicar filtro de Proyecto
            if st.session_state.filtro_proyecto and 'Proyecto' in df_filtrado_final.columns:
                df_filtrado_final = df_filtrado_final[df_filtrado_final['Proyecto'].isin(st.session_state.filtro_proyecto)]
            
            # Aplicar filtro de Prioridad
            if st.session_state.filtro_prioridad and 'Prioridad' in df_filtrado_final.columns:
                df_filtrado_final = df_filtrado_final[df_filtrado_final['Prioridad'].isin(st.session_state.filtro_prioridad)]
            
            # Aplicar filtro de Componente
            componente_col_final = None
            for nombre in posibles_nombres_componente:
                if nombre in df_filtrado_final.columns:
                    componente_col_final = nombre
                    break
            
            if st.session_state.filtro_componente and componente_col_final:
                df_filtrado_final = df_filtrado_final[df_filtrado_final[componente_col_final].isin(st.session_state.filtro_componente)]
            
            st.markdown("---")
            
            # --- MOSTRAR TABLAS FILTRADAS ---
            if 'Proyecto' in df_grilla.columns:
                # 1. Obtener los proyectos únicos del DataFrame filtrado
                proyectos_unicos_filtrados = df_filtrado_final['Proyecto'].dropna().drop_duplicates().sort_values().reset_index(drop=True)
                df_proyectos_unicos = pd.DataFrame(proyectos_unicos_filtrados, columns=['Proyecto Único'])
                
                # 2. Usar st.columns para crear el layout con las dos tablas
                col_unica, col_grilla = st.columns([1, 3])
                
                with col_unica:
                    st.markdown("**Lista de Proyectos Únicos**")
                    st.dataframe(
                        df_proyectos_unicos,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Mostrar estadísticas rápidas
                    st.metric("Proyectos mostrados", len(df_proyectos_unicos))
                
                with col_grilla:
                    st.markdown("**Datos Completos de la Grilla**")
                    # Mostrar el DataFrame filtrado
                    st.dataframe(
                        df_filtrado_final,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Mostrar contador de resultados
                    total_original = len(df_grilla)
                    total_filtrado = len(df_filtrado_final)
                    st.caption(f"📊 Mostrando {total_filtrado} de {total_original} registros ({total_filtrado/total_original*100:.1f}%)")
            
            # --- ESTADÍSTICAS DETALLADAS ---
            st.markdown("---")
            st.subheader("📈 Estadísticas")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                # Total de proyectos únicos en los resultados filtrados
                if 'Proyecto' in df_filtrado_final.columns:
                    proyectos_unicos = df_filtrado_final['Proyecto'].drop_duplicates()
                    total_proyectos_unicos = len(proyectos_unicos)
                    st.metric("Proyectos Únicos", total_proyectos_unicos)
                else:
                    st.metric("Registros", len(df_filtrado_final))
                    
            with col2:
                # Proyectos activos
                if estado_col and 'Proyecto' in df_filtrado_final.columns:
                    df_sin_duplicados = df_filtrado_final.drop_duplicates(subset=['Proyecto'], keep='first')
                    if 'Activo' in df_sin_duplicados[estado_col].values:
                        proyectos_activos_unicos = df_sin_duplicados[df_sin_duplicados[estado_col] == 'Activo'].shape[0]
                        st.metric("Proyectos Activos", proyectos_activos_unicos)
                    else:
                        st.metric("Proyectos Activos", 0)
                else:
                    st.metric("Registros Filtrados", len(df_filtrado_final))
                    
            with col3:
                # Distribución por estado
                if estado_col:
                    conteo_estados = df_filtrado_final[estado_col].value_counts()
                    if len(conteo_estados) > 0:
                        estado_principal = conteo_estados.index[0]
                        count_principal = conteo_estados.iloc[0]
                        st.metric("Estado Principal", f"{estado_principal} ({count_principal})")
                    else:
                        st.metric("Estado Principal", "Sin datos")
                else:
                    st.metric("Total Original", len(df_grilla))
                    
            with col4:
                # NUEVO: Distribución por Alistamiento
                if alistamiento_col:
                    conteo_alistamiento = df_filtrado_final[alistamiento_col].value_counts()
                    if len(conteo_alistamiento) > 0:
                        alistamiento_principal = conteo_alistamiento.index[0]
                        count_alistamiento = conteo_alistamiento.iloc[0]
                        st.metric("Alistamiento Principal", f"{alistamiento_principal} ({count_alistamiento})")
                    else:
                        st.metric("Alistamiento Principal", "Sin datos")
                else:
                    # Efectividad del filtro
                    total_original = len(df_grilla)
                    total_filtrado = len(df_filtrado_final)
                    porcentaje = (total_filtrado / total_original * 100) if total_original > 0 else 0
                    st.metric("Datos Mostrados", f"{porcentaje:.1f}%")
                    
        except FileNotFoundError:
            st.error("⚠️ No se encontró el archivo 'data/EstadoGrilla.xlsx'")
            st.info("Por favor, asegúrate de que el archivo existe en la carpeta 'data' del repositorio")
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")


    # ======================================================
    # TAB 7
    # ======================================================
    with tab7:
        st.subheader("📅 Cronograma de visitas")
        st.info("Programación de visitas de seguimiento e implementación metodologica Last Planner System en obra")


    # ======================================================
    # TAB 8: PULL PLANNING - DIAGRAMA DE GANTT
    # ======================================================
    with tab8:
        st.subheader("⏱️ Pull Planning - Diagrama de Gantt")
        
        # Intentar cargar el archivo CSV
        try:
            # Cargar el archivo CSV - nombres posibles
            nombres_posibles = [
                "data/pull_planning.csv",
                "data/cronograma.csv",
                "data/programacion.csv",
                "data/planning.csv"
            ]
            
            df_gantt = None
            archivo_encontrado = None
            
            for nombre_archivo in nombres_posibles:
                try:
                    df_gantt = pd.read_csv(nombre_archivo)
                    archivo_encontrado = nombre_archivo
                    break
                except FileNotFoundError:
                    continue
            
            if df_gantt is None:
                st.error("❌ No se encontró ningún archivo CSV de cronograma")
                st.info("""
                **Por favor, asegúrate de que el archivo esté en la carpeta `data/` con uno de estos nombres:**
                - `pull_planning.csv`
                - `cronograma.csv`
                - `programacion.csv`
                - `planning.csv`
                """)
                st.stop()
            
            st.success(f"✅ Archivo cargado: `{archivo_encontrado}`")
            
            # Verificar que las columnas requeridas existan
            columnas_requeridas = ['HC', 'Proyecto', 'Actividad', 'Inicio', 'Fin']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df_gantt.columns]
            
            if columnas_faltantes:
                st.error(f"❌ Faltan columnas requeridas: {', '.join(columnas_faltantes)}")
                st.info(f"📋 Columnas encontradas: {', '.join(df_gantt.columns.tolist())}")
                st.stop()
            
            # ========== PREPROCESAMIENTO DE DATOS ==========
            # Convertir fechas
            df_gantt['Inicio'] = pd.to_datetime(df_gantt['Inicio'], errors='coerce')
            df_gantt['Fin'] = pd.to_datetime(df_gantt['Fin'], errors='coerce')
            
            # Eliminar filas con fechas inválidas
            filas_originales = len(df_gantt)
            df_gantt = df_gantt.dropna(subset=['Inicio', 'Fin'])
            filas_validas = len(df_gantt)
            
            if filas_validas < filas_originales:
                st.warning(f"⚠️ Se eliminaron {filas_originales - filas_validas} filas con fechas inválidas")
            
            # Crear columna para display en Gantt
            df_gantt['Task_Display'] = df_gantt['HC'] + " - " + df_gantt['Actividad']
            
            # Calcular duración
            df_gantt['Duracion_Dias'] = (df_gantt['Fin'] - df_gantt['Inicio']).dt.days + 1
            df_gantt['Duracion_Dias'] = df_gantt['Duracion_Dias'].clip(lower=1)  # Mínimo 1 día
            
            # ========== PANEL DE INFORMACIÓN ==========
            with st.expander("📊 Información del dataset", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Actividades", len(df_gantt))
                with col2:
                    st.metric("Proyectos (HC)", df_gantt['HC'].nunique())
                with col3:
                    st.metric("Rango de fechas", 
                             f"{df_gantt['Inicio'].min().strftime('%d/%m/%Y')} - {df_gantt['Fin'].max().strftime('%d/%m/%Y')}")
                with col4:
                    st.metric("Días promedio/act", f"{df_gantt['Duracion_Dias'].mean():.1f}")
            
            # ========== BARRA LATERAL DE FILTROS ==========
            st.sidebar.markdown("---")
            st.sidebar.header("🔍 Filtros Pull Planning")
            
            # 1. FILTRO POR HC (PROYECTO) - CON BÚSQUEDA
            hc_options = sorted(df_gantt['HC'].dropna().unique().tolist())
            
            # Búsqueda rápida de HC
            buscar_hc = st.sidebar.text_input("🔎 Buscar HC:", placeholder="Ej: PROY-001")
            
            # Filtrar opciones basadas en búsqueda
            if buscar_hc:
                hc_filtrados = [hc for hc in hc_options if buscar_hc.lower() in str(hc).lower()]
            else:
                hc_filtrados = hc_options
            
            hc_seleccionados = st.sidebar.multiselect(
                "🏷️ Seleccionar HC (Proyectos):",
                options=hc_filtrados,
                default=hc_filtrados[:min(3, len(hc_filtrados))],
                help="HC es el identificador único de cada proyecto"
            )
            
            # 2. FILTRO POR NOMBRE DE PROYECTO
            if 'Proyecto' in df_gantt.columns:
                # Obtener proyectos únicos de los HC seleccionados
                if hc_seleccionados:
                    proyectos_disponibles = sorted(df_gantt[df_gantt['HC'].isin(hc_seleccionados)]['Proyecto'].dropna().unique().tolist())
                else:
                    proyectos_disponibles = sorted(df_gantt['Proyecto'].dropna().unique().tolist())
                
                proyecto_seleccionados = st.sidebar.multiselect(
                    "📋 Seleccionar por Nombre de Proyecto:",
                    options=proyectos_disponibles,
                    default=[]
                )
            else:
                proyecto_seleccionados = []
            
            # 3. FILTRO POR CÓDIGO DE PLANEACIÓN (si existe)
            codigo_seleccionados = []
            if 'CodigoPlaneacion' in df_gantt.columns:
                if hc_seleccionados:
                    codigos_disponibles = sorted(df_gantt[df_gantt['HC'].isin(hc_seleccionados)]['CodigoPlaneacion'].dropna().unique().tolist())
                else:
                    codigos_disponibles = sorted(df_gantt['CodigoPlaneacion'].dropna().unique().tolist())
                
                codigo_seleccionados = st.sidebar.multiselect(
                    "📐 Seleccionar Código de Planeación:",
                    options=codigos_disponibles,
                    default=[]
                )
            
            # 4. FILTRO POR RANGO DE FECHAS
            st.sidebar.markdown("---")
            st.sidebar.subheader("📅 Rango de Fechas")
            
            # Calcular fechas mínimas y máximas basadas en HC seleccionados
            if hc_seleccionados:
                fecha_min = df_gantt[df_gantt['HC'].isin(hc_seleccionados)]['Inicio'].min()
                fecha_max = df_gantt[df_gantt['HC'].isin(hc_seleccionados)]['Fin'].max()
            else:
                fecha_min = df_gantt['Inicio'].min()
                fecha_max = df_gantt['Fin'].max()
            
            # Convertir a date para st.date_input
            fecha_min_date = fecha_min.date() if hasattr(fecha_min, 'date') else fecha_min
            fecha_max_date = fecha_max.date() if hasattr(fecha_max, 'date') else fecha_max
            
            fecha_rango = st.sidebar.date_input(
                "Seleccionar rango de fechas:",
                value=(fecha_min_date, fecha_max_date),
                min_value=fecha_min_date,
                max_value=fecha_max_date
            )
            
            # 5. FILTRO POR DURACIÓN
            st.sidebar.markdown("---")
            st.sidebar.subheader("⏱️ Duración de Actividades")
            
            duracion_min = int(df_gantt['Duracion_Dias'].min())
            duracion_max = int(df_gantt['Duracion_Dias'].max())
            
            duracion_range = st.sidebar.slider(
                "Duración en días:",
                min_value=duracion_min,
                max_value=duracion_max,
                value=(duracion_min, duracion_max),
                help="Filtrar actividades por duración mínima y máxima"
            )
            
            # 6. BOTONES DE ACCIÓN
            st.sidebar.markdown("---")
            col_reset, col_expand = st.sidebar.columns(2)
            with col_reset:
                if st.button("🔄 Limpiar filtros", use_container_width=True):
                    st.rerun()
            with col_expand:
                expandir_todo = st.button("📊 Expandir todo", use_container_width=True)
            
            # ========== APLICAR FILTROS ==========
            df_filtrado = df_gantt.copy()
            filtros_aplicados = []
            
            # Aplicar filtro de HC
            if hc_seleccionados:
                df_filtrado = df_filtrado[df_filtrado['HC'].isin(hc_seleccionados)]
                filtros_aplicados.append(f"HC: {len(hc_seleccionados)}")
            
            # Aplicar filtro de nombre de proyecto
            if proyecto_seleccionados:
                df_filtrado = df_filtrado[df_filtrado['Proyecto'].isin(proyecto_seleccionados)]
                filtros_aplicados.append(f"Proyectos: {len(proyecto_seleccionados)}")
            
            # Aplicar filtro de código de planeación
            if codigo_seleccionados and 'CodigoPlaneacion' in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado['CodigoPlaneacion'].isin(codigo_seleccionados)]
                filtros_aplicados.append(f"Códigos: {len(codigo_seleccionados)}")
            
            # Aplicar filtro de fechas
            if len(fecha_rango) == 2:
                fecha_inicio_filtro = pd.to_datetime(fecha_rango[0])
                fecha_fin_filtro = pd.to_datetime(fecha_rango[1])
                
                df_filtrado = df_filtrado[
                    (df_filtrado['Fin'] >= fecha_inicio_filtro) & 
                    (df_filtrado['Inicio'] <= fecha_fin_filtro)
                ]
                filtros_aplicados.append(f"Fechas: {fecha_rango[0].strftime('%d/%m/%y')} a {fecha_rango[1].strftime('%d/%m/%y')}")
            
            # Aplicar filtro de duración
            df_filtrado = df_filtrado[
                (df_filtrado['Duracion_Dias'] >= duracion_range[0]) &
                (df_filtrado['Duracion_Dias'] <= duracion_range[1])
            ]
            
            # ========== MOSTRAR RESUMEN DE FILTROS ==========
            if filtros_aplicados:
                st.info(f"**Filtros activos:** {' | '.join(filtros_aplicados)} | **Actividades mostradas:** {len(df_filtrado)}")
            
            # ========== VISUALIZACIÓN PRINCIPAL ==========
            if not df_filtrado.empty:
                # Crear pestañas para diferentes vistas
                vista_gantt, vista_tabla, vista_resumen, vista_exportar = st.tabs([
                    "📊 Diagrama Gantt", 
                    "📋 Tabla de Datos", 
                    "📈 Resumen por HC",
                    "📤 Exportar"
                ])
                
                with vista_gantt:
                    st.markdown(f"### 🗺️ Diagrama de Gantt - {len(df_filtrado)} actividades")
                    
                    try:
                        import plotly.figure_factory as ff
                        import plotly.express as px
                        
                        # Preparar datos para Gantt
                        gantt_data = []
                        
                        # Asignar color por HC
                        hc_unicos = df_filtrado['HC'].dropna().unique()
                        colors = px.colors.qualitative.Set3
                        color_map = {}
                        
                        for i, hc in enumerate(hc_unicos):
                            color_map[hc] = colors[i % len(colors)]
                        
                        for _, row in df_filtrado.iterrows():
                            # Información para tooltip
                            tooltip_info = []
                            
                            if pd.notna(row.get('HC')):
                                tooltip_info.append(f"<b>HC:</b> {row['HC']}")
                            
                            if pd.notna(row.get('Proyecto')):
                                tooltip_info.append(f"<b>Proyecto:</b> {row['Proyecto']}")
                            
                            if pd.notna(row.get('CodigoPlaneacion')):
                                tooltip_info.append(f"<b>Código:</b> {row['CodigoPlaneacion']}")
                            
                            tooltip_info.append(f"<b>Duración:</b> {row['Duracion_Dias']} días")
                            
                            actividad = {
                                'Task': row['Task_Display'],
                                'Start': row['Inicio'],
                                'Finish': row['Fin'],
                                'Resource': row['HC'],
                                'Color': color_map.get(row['HC'], '#808080'),
                                'Complete': 100,  # Para visualización de progreso
                                'Description': '<br>'.join(tooltip_info)
                            }
                            
                            gantt_data.append(actividad)
                        
                        # Crear figura Gantt
                        fig = ff.create_gantt(
                            gantt_data,
                            colors=[act['Color'] for act in gantt_data],
                            index_col='Resource',
                            show_colorbar=True,
                            group_tasks=True,
                            showgrid_x=True,
                            showgrid_y=True,
                            bar_width=0.4,
                            title=f"Pull Planning - {len(hc_unicos)} Proyectos"
                        )
                        
                        # Personalizar layout
                        fig.update_layout(
                            height=max(600, len(gantt_data) * 30),
                            width=1000,
                            xaxis_title="Fecha",
                            yaxis_title="Actividades (HC - Actividad)",
                            showlegend=True,
                            hovermode='closest'
                        )
                        
                        # Formatear fechas en hover
                        fig.update_traces(
                            hovertemplate="<b>%{customdata[0]}</b><br>" +
                                         "Inicio: %{x|%d/%m/%Y}<br>" +
                                         "Fin: %{x2|%d/%m/%Y}<br>" +
                                         "%{customdata[1]}" +
                                         "<extra></extra>",
                            customdata=[[act['Task'], act['Description']] for act in gantt_data]
                        )
                        
                        # Mostrar gráfico
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Leyenda interactiva
                        with st.expander("🎨 Leyenda de colores por HC", expanded=False):
                            for hc, color in list(color_map.items())[:20]:  # Mostrar primeros 20
                                st.markdown(f"<span style='color:{color};font-weight:bold'>■</span> {hc}", 
                                          unsafe_allow_html=True)
                            
                            if len(color_map) > 20:
                                st.caption(f"... y {len(color_map) - 20} HC más")
                        
                    except Exception as e:
                        st.error(f"Error al crear el diagrama de Gantt: {e}")
                        st.info("Mostrando vista de tabla como alternativa")
                        st.dataframe(df_filtrado, use_container_width=True)
                
                with vista_tabla:
                    st.markdown("### 📋 Datos detallados del cronograma")
                    
                    # Estadísticas rápidas
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Actividades", len(df_filtrado))
                    with col2:
                        st.metric("Proyectos (HC)", df_filtrado['HC'].nunique())
                    with col3:
                        duracion_total = df_filtrado['Duracion_Dias'].sum()
                        st.metric("Días totales", duracion_total)
                    with col4:
                        fecha_min = df_filtrado['Inicio'].min().strftime('%d/%m')
                        fecha_max = df_filtrado['Fin'].max().strftime('%d/%m')
                        st.metric("Período", f"{fecha_min} - {fecha_max}")
                    
                    # Mostrar tabla con columnas ordenadas
                    columnas_orden = ['HC', 'Proyecto', 'Actividad', 'CodigoPlaneacion', 
                                    'Inicio', 'Fin', 'Duracion_Dias']
                    
                    # Filtrar columnas existentes
                    columnas_existentes = [col for col in columnas_orden if col in df_filtrado.columns]
                    
                    # Agregar columnas adicionales
                    columnas_adicionales = [col for col in df_filtrado.columns 
                                          if col not in columnas_existentes and col != 'Task_Display']
                    
                    columnas_finales = columnas_existentes + columnas_adicionales
                    
                    # Mostrar tabla
                    st.dataframe(
                        df_filtrado[columnas_finales],
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            'HC': st.column_config.TextColumn("HC", width="small"),
                            'Proyecto': st.column_config.TextColumn("Proyecto", width="medium"),
                            'Actividad': st.column_config.TextColumn("Actividad", width="large"),
                            'CodigoPlaneacion': st.column_config.TextColumn("Código", width="small"),
                            'Inicio': st.column_config.DateColumn("Inicio", format="DD/MM/YYYY"),
                            'Fin': st.column_config.DateColumn("Fin", format="DD/MM/YYYY"),
                            'Duracion_Dias': st.column_config.NumberColumn("Días", format="%d")
                        }
                    )
                
                with vista_resumen:
                    st.markdown("### 📈 Resumen por HC (Proyecto)")
                    
                    # Resumen estadístico por HC
                    resumen_hc = df_filtrado.groupby('HC').agg({
                        'Proyecto': 'first',
                        'Actividad': 'count',
                        'Inicio': 'min',
                        'Fin': 'max',
                        'Duracion_Dias': 'sum'
                    }).reset_index()
                    
                    resumen_hc = resumen_hc.rename(columns={
                        'Actividad': 'Total_Actividades',
                        'Duracion_Dias': 'Dias_Totales'
                    })
                    
                    # Calcular duración del proyecto
                    resumen_hc['Duracion_Proyecto'] = (resumen_hc['Fin'] - resumen_hc['Inicio']).dt.days + 1
                    
                    # Calcular densidad (actividades por día)
                    resumen_hc['Actividades_x_Dia'] = resumen_hc['Total_Actividades'] / resumen_hc['Duracion_Proyecto']
                    
                    # Ordenar por HC
                    resumen_hc = resumen_hc.sort_values('HC')
                    
                    # Mostrar tabla resumen
                    st.dataframe(
                        resumen_hc,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            'HC': "HC",
                            'Proyecto': "Proyecto",
                            'Total_Actividades': "Actividades",
                            'Inicio': st.column_config.DateColumn("Inicio", format="DD/MM/YYYY"),
                            'Fin': st.column_config.DateColumn("Fin", format="DD/MM/YYYY"),
                            'Duracion_Proyecto': "Días Proyecto",
                            'Dias_Totales': "Días Actividades",
                            'Actividades_x_Dia': st.column_config.NumberColumn("Act/Día", format="%.2f")
                        }
                    )
                    
                    # Gráficos de resumen
                    col_grafico1, col_grafico2 = st.columns(2)
                    
                    with col_grafico1:
                        try:
                            import plotly.express as px
                            
                            fig_actividades = px.bar(
                                resumen_hc,
                                x='HC',
                                y='Total_Actividades',
                                title='Actividades por HC',
                                color='HC',
                                text='Total_Actividades',
                                hover_data=['Proyecto', 'Duracion_Proyecto']
                            )
                            fig_actividades.update_traces(textposition='outside')
                            fig_actividades.update_layout(showlegend=False)
                            st.plotly_chart(fig_actividades, use_container_width=True)
                        except:
                            pass
                    
                    with col_grafico2:
                        try:
                            fig_timeline = px.timeline(
                                resumen_hc,
                                x_start="Inicio",
                                x_end="Fin",
                                y="HC",
                                color="HC",
                                title="Timeline por HC",
                                hover_data=['Proyecto', 'Total_Actividades']
                            )
                            fig_timeline.update_yaxes(autorange="reversed")
                            fig_timeline.update_layout(showlegend=False, height=400)
                            st.plotly_chart(fig_timeline, use_container_width=True)
                        except:
                            pass
                
                with vista_exportar:
                    st.markdown("### 📤 Exportar datos")
                    
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        st.markdown("#### Descargar datos filtrados")
                        
                        # Opción 1: CSV
                        csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Descargar como CSV",
                            data=csv_data,
                            file_name=f"pull_planning_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        # Opción 2: Excel
                        excel_buffer = BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df_filtrado.to_excel(writer, sheet_name='Pull_Planning', index=False)
                            # Agregar hoja de resumen
                            resumen_hc.to_excel(writer, sheet_name='Resumen_HC', index=False)
                        
                        excel_data = excel_buffer.getvalue()
                        
                        st.download_button(
                            label="📊 Descargar como Excel",
                            data=excel_data,
                            file_name=f"pull_planning_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    with col_export2:
                        st.markdown("#### Configuración de exportación")
                        
                        # Seleccionar columnas para exportar
                        columnas_export = st.multiselect(
                            "Seleccionar columnas para exportar:",
                            options=df_filtrado.columns.tolist(),
                            default=['HC', 'Proyecto', 'Actividad', 'Inicio', 'Fin', 'Duracion_Dias']
                        )
                        
                        if columnas_export:
                            df_export = df_filtrado[columnas_export]
                            
                            # Vista previa
                            with st.expander("👁️ Vista previa de datos a exportar"):
                                st.dataframe(df_export.head(10), use_container_width=True)
                            
                            # Exportar configuración personalizada
                            export_custom = df_export.to_csv(index=False).encode('utf-8')
                            
                            st.download_button(
                                label="📋 Descargar columnas seleccionadas",
                                data=export_custom,
                                file_name=f"pull_planning_personalizado_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                                mime="text/csv",
                                use_container_width=True,
                                key="custom_export"
                            )
            
            else:
                st.warning("⚠️ No hay actividades que coincidan con los filtros seleccionados")
                
                # Mostrar sugerencias
                with st.expander("💡 Sugerencias para ajustar filtros"):
                    st.markdown("""
                    1. **Reduce el número de HC seleccionados**
                    2. **Amplía el rango de fechas**
                    3. **Aumenta el rango de duración de actividades**
                    4. **Limpia los filtros** usando el botón en la barra lateral
                    """)
                
                # Mostrar vista previa de datos originales
                with st.expander("📁 Ver datos originales disponibles"):
                    st.dataframe(df_gantt.head(20), use_container_width=True)
                    st.caption(f"Total de {len(df_gantt)} actividades disponibles")
        
        except Exception as e:
            st.error(f"❌ Error al procesar los datos: {str(e)}")
            
            # Información de diagnóstico
            with st.expander("🔧 Información de diagnóstico"):
                st.code(f"Error: {str(e)}", language='python')
                
                # Listar archivos en data/
                try:
                    import os
                    archivos_data = os.listdir("data/") if os.path.exists("data/") else []
                    st.write("Archivos en carpeta data/:")
                    for archivo in archivos_data:
                        st.write(f"- {archivo}")
                except:
                    st.write("No se pudo listar archivos en data/")












# ----------------------------
# Ejecución principal
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
