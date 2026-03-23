import streamlit as st
from chatbot import agent_response
import requests

st.set_page_config(page_title="Antoniel AI - Portfólio")
st.title("🤖 Converse com o meu Currículo")
st.markdown(
    "Olá! Eu sou o assistente virtual do **Antoniel**. Pergunte-me sobre ele, habilidades, experiências ou formação!")

url = "http://127.0.0.1:8000/ask"

# (Session State)
# Se for a primeira vez que o usuário abre a página, criamos uma lista de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Como posso te ajudar a conhecer melhor o perfil do Antoniel?"}
    ]

# Deixa na tela todas as mensagens que já estão salvas na memória
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# A Caixa de Texto (Input) e a Lógica de Resposta
question = st.chat_input("Ex: Onde ele estudou?")

if question:
    # Mostra a pergunta do usuário na tela e salva na memória
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    user_input_dict = {
        "text": question
    }

    with st.chat_message("assistant"):
        with st.spinner("Analisando o currículo..."):
            try:
                response = requests.post(url, json=user_input_dict)
                response.raise_for_status()

                result = response.json()
                final_response = result["resposta"]

                st.markdown(final_response)

                st.session_state.messages.append({"role": "assistant", "content": final_response})
            except requests.exceptions.RequestException as e:
                st.error("Error connecting to the API.")

# if question:
#     # Mostra a pergunta do usuário na tela e salva na memória
#     with st.chat_message("user"):
#         st.markdown(question)
#     st.session_state.messages.append({"role": "user", "content": question})

#     # Chama a função agent_response
#     with st.chat_message("assistant"):
#         with st.spinner("Analisando o currículo..."):
#             response = agent_response(question)
#             st.markdown(response)

#     # Salva a resposta da IA na memória para não sumir no próximo recarregamento
#     st.session_state.messages.append({"role": "assistant", "content": response})