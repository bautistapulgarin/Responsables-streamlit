import streamlit as st 
import pandas as pd
import streamlit.components.v1 as components
import json

# ----------------------------
# Configuración general
# ----------------------------
st.set_page_config(page_title="Consulta de Responsables de Proyectos", layout="wide")

# ----------------------------
# Pantalla de Login
# ----------------------------
def login_screen():
    # Centramos contenido
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("loading.png", width=120)
        st.markdown(
            "<h2 style='text-align: center; margin-top: 10px;'>Acceso al Sistema</h2>",
            unsafe_allow_html=True
        )
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar", use_container_width=True):
            if password == st.secrets["password"]:
                st.session_state["logged_in"] = True
                st.success("✅ Acceso concedido")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")

# ----------------------------
# App principal
# ----------------------------
def main_app():
    # ----------------------------
    # Estilos personalizados
    # ----------------------------
    st.markdown(
        """
    <style>
        body { background-color: white !important; color: black !important; }
        .stApp { background-color: white !important; }
        :root { --blue-dark: #0a3d62; --blue-mid: #1f4e79; --blue-light: #eaf3fb; }
        .reportview-container, .main { background-color: var(--blue-light); }
        .css-1d391kg h1, .css-1d391kg h2 { color: var(--blue-dark); font-family: "Arial", sans-serif; }
        .stButton>button { background-color: var(--blue-mid); color: white; border-radius: 8px; border: none; padding: 8px 12px; font-weight: 600; }
        .stButton>button:hover { background-color: #163754; }
        .stSelectbox, .stDataFrame { border-radius: 10px; }
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
        st.image("loading.png", width=80)

    # ----------------------------
    # Tabs
    # ----------------------------
    tab1, tab2, tab3 = st.tabs([
        "📋 Responsables por Proyecto", 
        "📈 Reporte de Avances", 
        "🕒 Horario Reuniones LP"
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
    # TAB 2: Reporte de Avances
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
    # TAB 3: Horario Reuniones LP
    # ======================================================
    with tab3:
        st.subheader("🕒 Horario Reuniones LP")
        st.info("Filtra los horarios de reuniones Last Planner (LP) por Sucursal, Gerente o Proyecto.")

        try:
            df_horario = pd.read_excel("data/HorarioReuniones.xlsx")

            # Inicializar filtros en session_state
            for filtro in ["sucursal_lp", "gerente_lp", "proyecto_lp"]:
                if filtro not in st.session_state:
                    st.session_state[filtro] = []

            # Botón para restablecer filtros
            if st.button("Restablecer filtros LP"):
                for filtro in ["sucursal_lp", "gerente_lp", "proyecto_lp"]:
                    st.session_state[filtro] = []

            # Columnas de filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                sucursal_filtro = st.multiselect(
                    "Sucursal", sorted(df_horario["Sucursal"].dropna().unique()), key="sucursal_lp"
                )
            with col2:
                gerente_filtro = st.multiselect(
                    "Gerente", sorted(df_horario["Gerente"].dropna().unique()), key="gerente_lp"
                )
            with col3:
                proyecto_filtro = st.multiselect(
                    "Proyecto", sorted(df_horario["Proyecto"].dropna().unique()), key="proyecto_lp"
                )

            # Aplicar filtros
            df_filtrado = df_horario.copy()
            if sucursal_filtro:
                df_filtrado = df_filtrado[df_filtrado["Sucursal"].isin(sucursal_filtro)]
            if gerente_filtro:
                df_filtrado = df_filtrado[df_filtrado["Gerente"].isin(gerente_filtro)]
            if proyecto_filtro:
                df_filtrado = df_filtrado[df_filtrado["Proyecto"].isin(proyecto_filtro)]

            # Mostrar DataFrame filtrado
            st.dataframe(df_filtrado, use_container_width=True)

        except FileNotFoundError:
            st.error("⚠️ No se encontró el archivo 'data/HorarioReuniones.xlsx'")
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
