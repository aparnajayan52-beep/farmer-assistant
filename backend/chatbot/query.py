"""
query.py — Step 4 of Module 1 (AI Farming Chatbot)

What this script does:
1. Loads your Gemini API key from .env
2. Connects to your existing ChromaDB vector store
3. Takes a farmer's question, retrieves relevant chunks
4. Sends the question + chunks to Gemini
5. Returns a clean, natural-language answer

Run this from inside the backend/ folder with your venv active:
    python chatbot/query.py

Make sure you've already run store_embeddings.py at least once before this,
since this script expects the chroma_db folder to already exist.
"""

import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai

# ---- LOAD API KEY ----
load_dotenv()  # reads the .env file and loads variables into the environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---- CONNECT TO CHROMADB ----
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "farming_kb"

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embed_fn
)


def retrieve_context(query, n_results=6):
    """Finds the most relevant chunks from ChromaDB for a given question."""
    results = collection.query(query_texts=[query], n_results=n_results)
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    return chunks, sources


def answer_query(user_query, language="English"):
    """Retrieves context and generates a natural-language answer using Gemini."""
    chunks, sources = retrieve_context(user_query)
    context = "\n\n".join(chunks)

    prompt = f"""You are a helpful farming assistant for Indian farmers.
Answer the question in {language}, using ONLY the context provided below.
If the answer isn't in the context, say you don't have enough information rather than guessing.
Keep the answer clear, practical, and farmer-friendly (avoid overly technical jargon).

Context:
{context}

Question: {user_query}

Answer:"""

    response = model.generate_content(prompt)
    return {
        "answer": response.text,
        "sources": list(set(sources))  # unique source filenames used
    }


if __name__ == "__main__":
    # Quick manual test — try a few questions
    test_questions = [
        "What is the best season to grow paddy?",
        "How do I control pests in tomato plants?",
        "How should I fertilize coconut trees?"
    ]

    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"QUESTION: {q}")
        print('='*60)
        result = answer_query(q)
        print(f"\nANSWER:\n{result['answer']}")
        print(f"\nSOURCES USED: {result['sources']}")
