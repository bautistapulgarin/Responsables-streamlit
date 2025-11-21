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

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        " 🧑🏿 Responsables por Proyecto", 
        " 📈 Reporte de Avances", 
        " 🕰️ Horario Reuniones LP",
        " 📜 Directorio Documental",
        " 📋 Formulario",
        " 🏢 Proyectos en grilla"
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
            
            # Control único para el reset
            if "reset_counter" not in st.session_state:
                st.session_state.reset_counter = 0
            
            # Botón para restablecer filtros - SOLUCIÓN DEFINITIVA
            if st.button("🔄 Restablecer filtros", key="reset_filtros_grilla"):
                st.session_state.filtro_proyecto = []
                st.session_state.filtro_estado_grilla = []
                st.session_state.filtro_prioridad = []
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
                        key=f"estado_grilla_{st.session_state.reset_counter}"  # Clave única que cambia con cada reset
                    )
                    st.session_state.filtro_estado_grilla = filtro_estado_grilla
                else:
                    st.info("No hay columna de estado disponible")
            
            # Crear DataFrame base para filtros dependientes
            df_filtrado_base = df_grilla.copy()
            
            # Aplicar filtro de estado al DataFrame base para los otros filtros
            if st.session_state.filtro_estado_grilla and estado_col:
                df_filtrado_base = df_filtrado_base[df_filtrado_base[estado_col].isin(st.session_state.filtro_estado_grilla)]
            
            with col2:
                # SEGUNDO FILTRO: Proyecto (dependiente del estado) - CON CLAVE ÚNICA PARA RESET
                if 'Proyecto' in df_filtrado_base.columns:
                    # Las opciones de proyecto se basan en el DataFrame ya filtrado por estado
                    opciones_proyecto = sorted(df_filtrado_base['Proyecto'].dropna().unique().tolist())
                    filtro_proyecto = st.multiselect(
                        "📋 Proyecto",
                        options=opciones_proyecto,
                        default=st.session_state.filtro_proyecto,
                        key=f"proyecto_{st.session_state.reset_counter}"  # Clave única que cambia con cada reset
                    )
                    st.session_state.filtro_proyecto = filtro_proyecto
                else:
                    st.info("No hay columna 'Proyecto' disponible")
            
            # Aplicar filtro de proyecto al DataFrame base para prioridad
            if st.session_state.filtro_proyecto and 'Proyecto' in df_filtrado_base.columns:
                df_filtrado_base = df_filtrado_base[df_filtrado_base['Proyecto'].isin(st.session_state.filtro_proyecto)]
            
            # TERCER FILTRO: Prioridad (dependiente de estado y proyecto) - CON CLAVE ÚNICA PARA RESET
            col3, col4 = st.columns(2)
            
            with col3:
                # Filtro por Prioridad
                if 'Prioridad' in df_filtrado_base.columns:
                    opciones_prioridad = sorted(df_filtrado_base['Prioridad'].dropna().unique().tolist())
                    filtro_prioridad = st.multiselect(
                        "🎯 Prioridad",
                        options=opciones_prioridad,
                        default=st.session_state.filtro_prioridad,
                        key=f"prioridad_{st.session_state.reset_counter}"  # Clave única que cambia con cada reset
                    )
                    st.session_state.filtro_prioridad = filtro_prioridad
                else:
                    st.info("No hay columna 'Prioridad' disponible")
            
            with col4:
                # Mostrar estado actual de los filtros
                filtros_activos = False
                info_text = "🔍 **Estado de filtros:**\n\n"
                
                if st.session_state.filtro_estado_grilla:
                    info_text += f"• 📊 **Estado grilla:** {', '.join(st.session_state.filtro_estado_grilla)}\n"
                    filtros_activos = True
                else:
                    info_text += "• 📊 **Estado grilla:** Sin filtro\n"
                
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
                
                if filtros_activos:
                    st.success(info_text)
                else:
                    st.info(info_text)
            
            # APLICAR TODOS LOS FILTROS AL DATAFRAME FINAL
            df_filtrado_final = df_grilla.copy()
            
            # Aplicar filtro de Estado grilla
            if st.session_state.filtro_estado_grilla and estado_col:
                df_filtrado_final = df_filtrado_final[df_filtrado_final[estado_col].isin(st.session_state.filtro_estado_grilla)]
            
            # Aplicar filtro de Proyecto
            if st.session_state.filtro_proyecto and 'Proyecto' in df_filtrado_final.columns:
                df_filtrado_final = df_filtrado_final[df_filtrado_final['Proyecto'].isin(st.session_state.filtro_proyecto)]
            
            # Aplicar filtro de Prioridad
            if st.session_state.filtro_prioridad and 'Prioridad' in df_filtrado_final.columns:
                df_filtrado_final = df_filtrado_final[df_filtrado_final['Prioridad'].isin(st.session_state.filtro_prioridad)]
            
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

# ----------------------------
# Ejecución principal
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
