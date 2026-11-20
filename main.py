"""Week 2 — chatbot API with conversation memory (AI Engineering 90-day plan).

Builds on Week 1 in the same repo, same file. The only change: the
API now remembers what was said before, per session.

How it works:
- Each chat has a session_id (default "default"). Send the same
  session_id with every message in one conversation.
- The server keeps the last 10 messages (5 back-and-forths) for each
  session in memory, and sends that history to OpenAI with each new
  message — so follow-up questions make sense.
- POST /reset clears one session's memory. Restarting the server
  clears all memory: this is in-memory only, on purpose. Saving
  memory to a database is a later week.

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

app = FastAPI(title="Week 2 Chatbot API — with memory")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# How many messages to remember per session (5 exchanges).
MAX_HISTORY = 10

# session_id -> list of {"role": ..., "content": ...} messages.
# Plain dict on purpose: the lesson this week is the pattern,
# not a database.
sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    messages_remembered: int


class ResetRequest(BaseModel):
    session_id: str = "default"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = sessions.setdefault(req.session_id, [])
    history.append({"role": "user", "content": req.message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer briefly."},
            *history,
        ],
    )
    reply = response.choices[0].message.content or ""
    history.append({"role": "assistant", "content": reply})

    # Keep only the most recent messages, so the history never
    # grows forever (and never blows up the token bill).
    del history[: -MAX_HISTORY]

    return ChatResponse(
        reply=reply,
        session_id=req.session_id,
        messages_remembered=len(history),
    )


@app.post("/reset")
def reset(req: ResetRequest):
    sessions.pop(req.session_id, None)
    return {"status": "ok", "session_id": req.session_id, "message": "memory cleared"}
