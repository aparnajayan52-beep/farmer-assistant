"""
ingest.py — Step 2 of Module 1 (AI Farming Chatbot)

What this script does:
1. Reads every PDF inside data/knowledge_base/
2. Extracts the raw text from each PDF
3. Splits that text into overlapping chunks (small pieces the chatbot can search over)
4. Prints a summary so you can verify everything worked correctly

Run this from inside the backend/ folder with your venv active:
    python chatbot/ingest.py
"""

import os
from pypdf import PdfReader

# ---- CONFIG ----
# Path to the knowledge base folder (relative to backend/)
KNOWLEDGE_BASE_DIR = os.path.join("..", "data", "knowledge_base")

CHUNK_SIZE = 500      # characters per chunk
CHUNK_OVERLAP = 50    # overlap between chunks, so context isn't lost at boundaries


def extract_text_from_pdf(pdf_path):
    """Reads a PDF file and returns all its text as one big string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Splits a long string of text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:  # skip empty chunks
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def process_knowledge_base():
    """Main function: processes every PDF in the knowledge_base folder."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"ERROR: Folder not found: {KNOWLEDGE_BASE_DIR}")
        return []

    pdf_files = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in knowledge_base folder.")
        return []

    print(f"Found {len(pdf_files)} PDF(s): {pdf_files}\n")

    all_chunks = []  # will hold dicts: {"text": chunk, "source": filename}

    for filename in pdf_files:
        filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
        print(f"Processing: {filename} ...")

        try:
            text = extract_text_from_pdf(filepath)
        except Exception as e:
            print(f"  Failed to read {filename}: {e}")
            continue

        if not text.strip():
            print(f"  WARNING: No extractable text found in {filename} (might be a scanned/image PDF).")
            continue

        chunks = chunk_text(text)
        print(f"  Extracted {len(text)} characters -> {len(chunks)} chunks")

        for chunk in chunks:
            all_chunks.append({"text": chunk, "source": filename})

    print(f"\nTOTAL CHUNKS ACROSS ALL FILES: {len(all_chunks)}")

    # Show one sample chunk so you can eyeball the quality of extraction
    if all_chunks:
        print("\n--- SAMPLE CHUNK (first one) ---")
        print(f"Source: {all_chunks[0]['source']}")
        print(all_chunks[0]["text"][:300])
        print("--- END SAMPLE ---")

    return all_chunks


if __name__ == "__main__":
    chunks = process_knowledge_base()
