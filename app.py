import streamlit as st 
import pandas as pd
import streamlit.components.v1 as components
import json
import unicodedata
import os

# ----------------------------
# Configuración general
# ----------------------------
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")

# ----------------------------
# Pantalla de Login
# ----------------------------
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Ajusta la imagen si la tienes
        try:
            st.image("loading.png", width=120)
        except Exception:
            pass

        st.markdown(
            "<h2 style='text-align: center; margin-top: 10px;'>Acceso al Sistema</h2>",
            unsafe_allow_html=True
        )

        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar", use_container_width=True):
            if "password" in st.secrets and password == st.secrets["password"]:
                st.session_state["logged_in"] = True
                st.success("✅ Acceso concedido")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")

# ----------------------------
# Util: normalizar nombre de columnas (quita tildes, espacios, pone mayúsculas)
# ----------------------------
def normalize_col(name: str) -> str:
    if not isinstance(name, str):
        name = str(name)
    s = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    s = s.strip().upper().replace(" ", "_")
    # también reemplazar dobles guiones bajos
    while "__" in s:
        s = s.replace("__", "_")
    return s

# ----------------------------
# App principal
# ----------------------------
def main_app():
    # ----------------------------
    # Estilos personalizados (mantengo tu estilo)
    # ----------------------------
    st.markdown(
        """
    <style>
        body { background-color: white !important; color: black !important; }
        .stApp { background-color: white !important; }

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
    </style>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------
    # Encabezado con logo
    # ----------------------------
    col_title, col_logo = st.columns([6, 1])
    with col_title:
        st.title("Consulta de Responsables de Proyectos")
    with col_logo:
        try:
            st.image("loading.png", width=80)
        except Exception:
            pass

    # ----------------------------
    # Tabs (restauro tu primer diseño)
    # ----------------------------
    tab1, tab2, tab3 = st.tabs(["📋 Responsables por Proyecto", "📈 Reporte de Avances", "🕒 Horario de Reuniones"])

    # ======================================================
    # TAB 1: Responsables (restaurada a la versión original que funcionaba)
    # ======================================================
    with tab1:
        def load_data_responsables():
            return pd.read_excel("data/ResponsablesPorProyecto.xlsx")

        df = load_data_responsables()

        # inicializar session_state para filtros (como en tu versión original)
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
            # en tu código original buscabas los gerentes en Cargo == "Gerente de proyectos"
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
    # TAB 2: Reporte de Avances (igual que antes)
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
    # TAB 3: Horario de Reuniones (robusto, con normalización)
    # ======================================================
    with tab3:
        st.subheader("🕒 Horario de Reuniones - Last Planner System")
        # Intentar abrir el archivo con nombre exacto proporcionado, si no existe, intentar otras variantes
        posibles_rutas = [
            "data/HorarioReuniones.xlsx",
            "data/HorariosReuniones.xlsx",
            "data/13. Horarios Reuniones Last Planner 2025.xlsx",
            "data/HorariosReuniones 2025.xlsx"
        ]
        df_reuniones = None
        ruta_encontrada = None
        for r in posibles_rutas:
            if os.path.exists(r):
                try:
                    df_reuniones = pd.read_excel(r)
                    ruta_encontrada = r
                    break
                except Exception:
                    # si existe pero no puede leerse, reportar error
                    st.error(f"Se encontró el archivo {r} pero hubo un error al leerlo.")
                    df_reuniones = None
                    ruta_encontrada = r
                    break

        if df_reuniones is None:
            st.error("No se encontró el archivo de horarios. Busqué:\n- " + "\n- ".join(posibles_rutas) + "\n\nPor favor sube 'HorarioReuniones.xlsx' (o 'HorariosReuniones.xlsx') a la carpeta data.")
        else:
            # Normalizar nombres de columnas para evitar errores por tildes/espacios/diferentes capitalizaciones
            df_reuniones = df_reuniones.copy()
            original_cols = list(df_reuniones.columns)
            normalized_map = {c: normalize_col(c) for c in original_cols}
            df_reuniones.rename(columns=normalized_map, inplace=True)

            # columnas esperadas normalizadas
            expected = {
                "SUCURSAL": "SUCURSAL",
                "PRACTICANTE": "PRACTICANTE",
                "GERENTE": "GERENTE",
                "PROYECTO": "PROYECTO",
                "DIA_INTERMEDIA": "DIA_INTERMEDIA",
                "HORA_INTERMEDIA": "HORA_INTERMEDIA",
                "DIA_SEMANAL": "DIA_SEMANAL",
                "HORA_SEMANAL": "HORA_SEMANAL"
            }

            # comprobar cuáles columnas están disponibles
            cols_presentes = set(df_reuniones.columns)
            # Si faltan las columnas mínimas, avisar
            min_req = {"SUCURSAL", "GERENTE", "PROYECTO"}
            if not min_req.issubset(cols_presentes):
                st.error(f"El archivo '{ruta_encontrada}' no contiene las columnas mínimas esperadas. Columnas encontradas: {sorted(list(cols_presentes))}")
            else:
                # Preparar filtros (usar valores únicos existentes)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    sucursal_vals = sorted(df_reuniones["SUCURSAL"].dropna().unique().tolist())
                    sucursal = st.multiselect("Sucursal", sucursal_vals)
                with col2:
                    proyecto_vals = sorted(df_reuniones["PROYECTO"].dropna().unique().tolist())
                    proyecto = st.multiselect("Proyecto", proyecto_vals)
                with col3:
                    gerente_vals = sorted(df_reuniones["GERENTE"].dropna().unique().tolist())
                    gerente = st.multiselect("Gerente", gerente_vals)
                with col4:
                    tipo_reunion = st.selectbox("Tipo de reunión", ["Intermedia", "Semanal"])

                df_filtrado = df_reuniones.copy()
                if sucursal:
                    df_filtrado = df_filtrado[df_filtrado["SUCURSAL"].isin(sucursal)]
                if proyecto:
                    df_filtrado = df_filtrado[df_filtrado["PROYECTO"].isin(proyecto)]
                if gerente:
                    df_filtrado = df_filtrado[df_filtrado["GERENTE"].isin(gerente)]

                # según el tipo seleccionado, mapear columnas Día/Hora
                if tipo_reunion == "Intermedia":
                    dia_col = "DIA_INTERMEDIA"
                    hora_col = "HORA_INTERMEDIA"
                else:
                    dia_col = "DIA_SEMANAL"
                    hora_col = "HORA_SEMANAL"

                # si las columnas específicas no existen, mostrarlas vacías con aviso
                if dia_col not in df_filtrado.columns:
                    df_filtrado[dia_col] = pd.NA
                if hora_col not in df_filtrado.columns:
                    df_filtrado[hora_col] = pd.NA

                # filtros extra por día/hora (si existen valores)
                col5, col6 = st.columns(2)
                with col5:
                    dia_vals = sorted(df_filtrado[dia_col].dropna().unique().tolist())
                    dia = st.multiselect("Día", dia_vals)
                with col6:
                    hora_vals = sorted(df_filtrado[hora_col].dropna().unique().tolist())
                    hora = st.multiselect("Hora", hora_vals)

                if dia:
                    df_filtrado = df_filtrado[df_filtrado[dia_col].isin(dia)]
                if hora:
                    df_filtrado = df_filtrado[df_filtrado[hora_col].isin(hora)]

                # Preparar columnas para mostrar (usar nombres originales si quieres, aquí muestro una selección clara)
                display_cols = []
                # intentar usar la columna Practicante si existe
                if "PRACTICANTE" in df_filtrado.columns:
                    display_cols.append("PRACTICANTE")
                display_cols += ["SUCURSAL", "GERENTE", "PROYECTO", dia_col, hora_col]

                # renombrar columnas mostradas a una forma legible (opcional)
                rename_display = {
                    "SUCURSAL": "Sucursal",
                    "PRACTICANTE": "Practicante",
                    "GERENTE": "Gerente",
                    "PROYECTO": "Proyecto",
                    "DIA_INTERMEDIA": "Día Intermedia",
                    "HORA_INTERMEDIA": "Hora Intermedia",
                    "DIA_SEMANAL": "Día Semanal",
                    "HORA_SEMANAL": "Hora Semanal"
                }

                # Mostrar resultados
                st.markdown("---")
                if not df_filtrado.empty:
                    df_show = df_filtrado[display_cols].copy()
                    # renombrar columnas para presentación
                    df_show.rename(columns={c: rename_display.get(c, c) for c in df_show.columns}, inplace=True)
                    st.dataframe(df_show, use_container_width=True)

                    # descarga CSV del filtrado (opcional, creo que antes pediste no, pero lo dejo disponible)
                    csv = df_show.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Descargar horarios filtrados", csv, file_name="HorarioReuniones_filtrado.csv", mime="text/csv")
                else:
                    st.info("No se encontraron reuniones con los filtros seleccionados.")

# ----------------------------
# Ejecución principal
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()
