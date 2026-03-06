from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

emb = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001')

def retrieve(quest):
    db = Chroma(
        persist_directory = './chroma_db',
        embedding_function = emb
    )

    results = db.similarity_search(
        query = quest,
        k=2
    )

    return results

if __name__ == "__main__":
    ask = "Onde ele fez mestrado?"

    ans = retrieve(ask)

    for i in ans:
        print(i.metadata)
        print(i.page_content)
        print("="*20)