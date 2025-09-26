import streamlit as st

st.title("Calculadora Simple - Suma de 2 números")

num1 = st.number_input("Ingrese el primer número", value=0.0)
num2 = st.number_input("Ingrese el segundo número", value=0.0)

if st.button("Calcular suma"):
    resultado = num1 + num2
    st.success(f"El resultado es: {resultado}")
