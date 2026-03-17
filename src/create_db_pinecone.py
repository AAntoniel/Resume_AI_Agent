import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from data_loader import data_loader

load_dotenv()

index_name = "my-resume"
emb = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')
path = "data/curriculo_pt.md"

def load_vectorstore(data):
# '.from_documents' vem da classe 'vectorstore' e serve para desempacotar o objeto document criado em 'data_loader' 
    chunks = data_loader(data)

    PineconeVectorStore.from_documents(
        documents = chunks,
        embedding = emb,
        index_name = index_name
    )

if __name__ == "__main__":
    load_vectorstore(path)