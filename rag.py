from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

db_dir = "./chroma_db"

emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_vectorstore():
    return Chroma(
        persist_directory = db_dir,
        embedding_function = emb
    )

def retrieve(query, k=3):
    db = load_vectorstore()
    docs = db.similarity_search(query, k=k)
    return docs