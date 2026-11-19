"""Week 1 starter — first chatbot API (AI Engineering 90-day plan).

Run it, then put it on GitHub. That's the Week 1 milestone:
a simple chatbot API on GitHub.

Requires: Python 3.11, an OpenAI API key.
  pip install fastapi uvicorn openai
  set OPENAI_API_KEY=sk-...        (Windows PowerShell: $env:OPENAI_API_KEY="sk-...")
  uvicorn main:app --reload
  Open http://127.0.0.1:8000/docs to try it.
"""
import os

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI(title="Week 1 Chatbot API")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer briefly."},
            {"role": "user", "content": req.message},
        ],
    )
    return ChatResponse(reply=response.choices[0].message.content or "")
