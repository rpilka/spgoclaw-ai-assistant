from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from rag import search_knowledge

app = FastAPI()
client = OpenAI()

SYSTEM_PROMPT = """Jesteś wirtualnym asystentem Szkoły Podstawowej w Gocławiu. Odpowiadasz po polsku."""

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    docs = search_knowledge(req.message)
    context = "\n\n".join([d["content"] for d in docs]) if docs else ""
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"system","content":f"KONTEKST:\n{context}"},
            {"role":"user","content":req.message}
        ]
    )
    return {"answer": completion.choices[0].message.content}
