from fastapi import FastAPI
from pydantic import BaseModel
from rag import retrieve
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Criando o client corretamente
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

app = FastAPI()

class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(request: QueryRequest):

    docs = retrieve(request.question)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    Você é um assistente que responde perguntas sobre o currículo de Antoniel.

    Contexto:
    {context}

    Pergunta:
    {request.question}

    Responda de forma profissional e objetiva.
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return {"answer": response.text}