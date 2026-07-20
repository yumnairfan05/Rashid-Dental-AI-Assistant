import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Load FAISS index
index = faiss.read_index("faiss_index.bin")


def retrieve_context(query, top_k=3):
    """
    Find relevant knowledge base chunks
    """

    query_embedding = model.encode([query])

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


def generate_answer(query):
    """
    Generate response using retrieved context
    """

    context = retrieve_context(query)

    prompt = f"""
    You are Rashid Dental AI Assistant.

    Answer only using this information:

    {context}

    User Question:
    {query}
    """

    # Later connect LLM here
    return prompt