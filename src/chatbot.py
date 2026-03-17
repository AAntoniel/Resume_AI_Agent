from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_chroma import Chroma
from langchain_pinecone import PineconeVectorStore

from datetime import datetime

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

emb = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')

def retrieve(quest):
    # db = Chroma(
    #     persist_directory = './chroma_db',
    #     embedding_function = emb
    # )
    db = PineconeVectorStore(
        index_name="my-resume",
        embedding = emb
    )

    results = db.similarity_search(
        query = quest,
        k=2
    )

    # Results retorna uma lista de objetos, mas o modelo não le objetos, e sim textos. Abaixo, extrai-se apenas os textos.  Passa os metadados, 
    # Como os títulos e junta com o conteúdo para dar o contexto completo para a IA
    retrieve_texts = []

    for doc in results:
        title = " > ".join(doc.metadata.values())
        complete_content = f"[{title}]\n{doc.page_content}"

        retrieve_texts.append(complete_content)

    retrieve_context = "\n\n".join(retrieve_texts)

    return retrieve_context


model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature = 0.2,
)

today = datetime.now().strftime("%B de %Y")

template = ChatPromptTemplate([
    ("system", """Você é o assistente virtual do Antoniel. Responda as perguntas dos rcrutadores de forma profissional e simpátca, usando apenas o contexto 
                  fornecido abaixo.
     
                  INFORMAÇÃO TEMPORAL IMPORTANTE: A data de hoje é {today}. Compare essa data com as presentes nos contextos para utilizar o tempo
                  verbal correto.
     
                  CONTEXTO DO CURRÍCULO: {context}. 
     
                  Se a resposta não existir no contexto, diga que não sabe."""),
    ("human", "{user_input}")
])

if __name__ == "__main__":
    ask = "Quais são as experiências do Antoniel?"

    context = retrieve(ask)

    prompt_value = template.invoke({
        "context": context,
        "user_input": ask,
        "today": today
    })

    response = model.invoke(prompt_value)

    print(response)
    print("="*20)
    print(response.content)