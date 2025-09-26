import streamlit as st
import pandas as pd

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_excel("ResponsablesPorProyecto.xlsx")

df = load_data()

st.title("🔎 Consulta de Responsables por Proyecto")

# Campo de entrada libre
pregunta = st.text_input("Haz tu consulta (ejemplo: 'quién es el Director de obra del proyecto Burdeos Ciudad La Salle')")

def responder_pregunta(pregunta):
    pregunta = pregunta.lower()

    # Buscar por proyecto
    if "proyecto" in pregunta:
        for proyecto in df["Proyecto"].unique():
            if proyecto.lower() in pregunta:
                filtro = df[df["Proyecto"].str.lower() == proyecto.lower()]
                break
        else:
            return "❌ No encontré el proyecto en la base de datos."

    # Buscar por sucursal
    elif "sucursal" in pregunta:
        for sucursal in df["Sucursal"].unique():
            if sucursal.lower() in pregunta:
                filtro = df[df["Sucursal"].str.lower() == sucursal.lower()]
                break
        else:
            return "❌ No encontré la sucursal en la base de datos."

    # Buscar por cluster
    elif "cluster" in pregunta:
        for cluster in df["Cluster"].unique():
            if cluster.lower() in pregunta:
                filtro = df[df["Cluster"].str.lower() == cluster.lower()]
                break
        else:
            return "❌ No encontré el cluster en la base de datos."

    # Buscar por gerencia (campo HC o Responsable que contenga nombre de gerente)
    elif "gerencia" in pregunta or "gerente" in pregunta:
        for gerente in df["Responsable"].unique():
            if gerente.lower() in pregunta:
                filtro = df[df["Responsable"].str.lower() == gerente.lower()]
                break
        else:
            return "❌ No encontré el gerente en la base de datos."

    else:
        return "❌ No entendí tu pregunta. Intenta incluir palabras como 'proyecto', 'sucursal', 'cluster' o 'gerente'."

    # Buscar cargo dentro de la pregunta
    cargo_encontrado = None
    for cargo in df["Cargo"].unique():
        if cargo.lower() in pregunta:
            cargo_encontrado = cargo
            break

    if cargo_encontrado:
        filtro = filtro[filtro["Cargo"].str.lower() == cargo_encontrado.lower()]

    if filtro.empty:
        return "❌ No encontré responsables con esos criterios."

    return filtro[["Sucursal", "Cluster", "Proyecto", "Cargo", "Responsable", "Correo", "Celular"]]

# Procesar pregunta
if pregunta:
    respuesta = responder_pregunta(pregunta)
    if isinstance(respuesta, pd.DataFrame):
        st.write("### ✅ Resultados encontrados:")
        st.dataframe(respuesta)
    else:
        st.warning(respuesta)
