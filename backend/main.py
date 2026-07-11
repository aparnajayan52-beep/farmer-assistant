
"""
main.py — FastAPI entrypoint for the Farmer Assistant backend
 
Exposes:
  POST /chat     — AI farming chatbot (Module 1)
  POST /schemes  — Government scheme recommender (Module 2)
 
Run this from inside the backend/ folder with your venv active:
    uvicorn main:app --reload
"""
 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
from chatbot.query import answer_query
from schemes.match import get_eligible_schemes
 
app = FastAPI(title="Farmer Assistant API")
 
# ---- CORS SETUP ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
 
 
class SchemeRequest(BaseModel):
    state: str
    crop: str
    land_size_category: str = "Any"
    income_category: str = "All Farmers"
 
 
# ---- ROUTES ----
@app.get("/")
def read_root():
    return {"message": "Farmer Assistant API is running"}
 
 
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """AI chatbot answer using RAG pipeline (Module 1)."""
    result = answer_query(request.query, request.language)
    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }
 
 
@app.post("/schemes")
def schemes(request: SchemeRequest):
    """Returns eligible government schemes based on farmer inputs (Module 2)."""
    results = get_eligible_schemes(
        state=request.state,
        crop=request.crop,
        land_size_category=request.land_size_category,
        income_category=request.income_category
    )
    return {"schemes": results, "count": len(results)}