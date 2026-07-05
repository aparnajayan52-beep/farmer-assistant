"""
main.py — FastAPI entrypoint for the Farmer Assistant backend
 
This exposes a /chat endpoint that the Next.js frontend will call.
It reuses the answer_query() function from chatbot/query.py.
 
Run this from inside the backend/ folder with your venv active:
    uvicorn main:app --reload
"""
 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
from chatbot.query import answer_query
 
app = FastAPI(title="Farmer Assistant API")
 
# ---- CORS SETUP ----
# This allows your Next.js frontend (running on localhost:3000) to call this API
# (running on localhost:8000). Without this, the browser blocks the request.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
# ---- REQUEST/RESPONSE MODELS ----
class ChatRequest(BaseModel):
    query: str
    language: str = "English"
 
 
class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
 
 
# ---- ROUTES ----
@app.get("/")
def read_root():
    return {"message": "Farmer Assistant API is running"}
 
 
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Takes a farmer's question and returns an AI-generated answer
    grounded in the knowledge base (RAG pipeline).
    """
    result = answer_query(request.query, request.language)
    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }