from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from data_loader import data_loader

load_dotenv()

emb = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')

path = "data/curriculo_pt.md"

def load_vectorstore(data):
# '.from_documents' vem da classe 'vectorstore' e serve para desempacotar o objeto document criado em 'data_loader' 
    chunks = data_loader(data)

    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = emb,
        persist_directory = './chroma_db'
    )

if __name__ == "__main__":
    load_vectorstore("data/curriculo_pt.md")