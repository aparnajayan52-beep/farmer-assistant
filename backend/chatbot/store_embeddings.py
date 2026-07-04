"""
store_embeddings.py — Step 3 of Module 1 (AI Farming Chatbot)
"""

import chromadb
from chromadb.utils import embedding_functions
from ingest import process_knowledge_base

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "farming_kb"


def build_vector_store():
    print("Step 1: Extracting and chunking all PDFs...\n")
    chunks = process_knowledge_base()

    if not chunks:
        print("No chunks to store. Check your knowledge_base folder.")
        return

    print(f"\nStep 2: Setting up ChromaDB at '{CHROMA_DB_PATH}'...")

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn
    )

    print(f"Step 3: Adding {len(chunks)} chunks to the collection...")
    print("(This may take a minute or two the first time — it's downloading an embedding model.)\n")

    documents = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    BATCH_SIZE = 100
    for i in range(0, len(documents), BATCH_SIZE):
        batch_docs = documents[i:i + BATCH_SIZE]
        batch_meta = metadatas[i:i + BATCH_SIZE]
        batch_ids = ids[i:i + BATCH_SIZE]

        collection.add(
            documents=batch_docs,
            metadatas=batch_meta,
            ids=batch_ids
        )
        print(f"  Added chunks {i} to {i + len(batch_docs)}")

    print(f"\nDONE. Total chunks stored: {collection.count()}")
    return collection


def test_query(collection, query_text, n_results=3):
    print(f"\n--- TEST QUERY: '{query_text}' ---")
    results = collection.query(query_texts=[query_text], n_results=n_results)

    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        print(f"\nResult {i + 1} (from {source}):")
        print(doc[:300])


if __name__ == "__main__":
    collection = build_vector_store()

    if collection:
        test_query(collection, "How to control pests in tomato plants?")
        test_query(collection, "What is the best season to grow paddy?")