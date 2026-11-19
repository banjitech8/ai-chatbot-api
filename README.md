# Week 1 — First chatbot API

Goal: get GitHub set up properly and ship this simple chatbot API.
Time: about 30–45 minutes, in small steps. No rush — this is for
when you have a free evening, now that the discovery gathering is
parked waiting on Mr. Blankenship.

## 1. Set up the project (10 min)
```powershell
mkdir ai-chatbot-api
cd ai-chatbot-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn openai
```
Copy `main.py` from this starter folder into `ai-chatbot-api`.

## 2. Run it (5 min)
```powershell
$env:OPENAI_API_KEY="sk-..."
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs, try `POST /chat` with
`{"message": "Hello"}`. If it replies, the API works.

## 3. Put it on GitHub (15 min)
1. On github.com, create a new public repo named `ai-chatbot-api`.
   Do not add a README there — you already have one locally.
2. In the project folder:
```powershell
git init
git add main.py README.md
git commit -m "Week 1: first chatbot API (FastAPI + OpenAI)"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-chatbot-api.git
git push -u origin main
```
3. Add a `.gitignore` with `.venv/` and `.env` in it before any
   later commit — never commit your API key.

## What this proves (for the portfolio)
- FastAPI endpoint with request/response models
- Calling the OpenAI API with a system prompt
- A repo with a real, runnable project — the Days 1–30 milestone

## Next, when ready
- Add a short README section describing what it does (already here).
- Week 2 idea: keep a short conversation history in memory, so
  follow-up messages remember what was said before.

Note: the success-definition question (paid job vs job-ready
portfolio vs first freelance project) is still open — the plan
already aims at job-ready with a portfolio, so this step fits
whichever one you pick.
