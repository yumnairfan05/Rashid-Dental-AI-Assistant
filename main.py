from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from chatbot import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("faiss_index.bin")

# Load text chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


@app.get("/")
def home():
    return {
        "message": "Rashid Dental AI Backend Running"
    }


@app.post("/chat")
def chat(data: dict):

    question = data["question"]

    query_embedding = embedding_model.encode([question])

    distances, indices = index.search(
        np.array(query_embedding),
        3
    )

    context = ""

    for i in indices[0]:
        context += chunks[i] + "\n\n"

    # Generate AI answer
    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "source": "Knowledge Base"
    }