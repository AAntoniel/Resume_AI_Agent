import streamlit as st
import requests

st.title("Pergunte sobre meu currículo")

question = st.text_input("Digite sua pergunta:")

if st.button("Enviar"):
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )
    
    st.write(response.json()["answer"])