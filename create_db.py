
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
# import markdown

db_dir = "./chroma_db"

def create_db():
    print("Reading MD file.")
    with open("data/curriculo_pt.md", "r", encoding="utf-8") as f:
        md_file = f.read()

    # Split the text based on the markdown headers
    print("Splitting text (chunks)")
    headers = [("\#", "Header 1"),
               ("\#\#", "Header 2"),]
    
    markdown_splitters = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
    chunks = markdown_splitters.split_text(md_file)

    print(f"{len(chunks)} splits created.")

    print("Loading embedding model")

    emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Generating Embedding and saving in ChromaDB.")
    
    try:
        Chroma.from_documents(documents=chunks,
                          embedding=emb,
                          persist_directory=db_dir)
        print("Success! Database created!")
    except Exception as e:
        print("Error! There was a problem creating the Database!", e)

if __name__ == "__main__":
    create_db()
