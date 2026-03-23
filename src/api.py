from fastapi import FastAPI
from pydantic import BaseModel
from src.chatbot import agent_response

app = FastAPI(
    title="API Resume AI",
    description="Backend para o assistente virtual do meu portfólio."
)

class Question(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "API online!"}

@app.post("/ask")
def make_question(user_input: Question):
    print(f"Recebi a pergunta: {user_input.text}")

    ai_response = agent_response(user_input.text)

    return {"resposta": ai_response}

