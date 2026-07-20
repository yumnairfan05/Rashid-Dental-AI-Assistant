# 🦷 Rashid Dental AI Assistant

An AI-powered chatbot developed for **Rashid Dental Clinic** to answer patient queries using a Retrieval-Augmented Generation (RAG) pipeline based on a verified Markdown knowledge base.

---

## 📌 Project Objective

The objective of this project is to build an intelligent dental clinic assistant that can:

- Answer clinic-related questions using verified knowledge
- Provide information about dental services
- Guide patients through the appointment process
- Respond safely to medical-related questions
- Support future appointment booking functionality
- Be integrated into the clinic website

---

## ✨ Features

- AI-powered chatbot using Google Gemini
- FastAPI backend
- Responsive HTML/CSS/JavaScript frontend
- Retrieval-Augmented Generation (RAG)
- Markdown Knowledge Base
- Semantic search using Sentence Transformers
- FAISS vector search
- Context-aware responses
- Source-aware answers
- Safety guardrails for medical queries
- Environment variable support
- CORS enabled backend

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Google Gemini API
- Sentence Transformers
- FAISS
- NumPy
- Pickle

### Frontend

- HTML
- CSS
- JavaScript

### AI & NLP

- Google Gemini
- all-MiniLM-L6-v2 Embedding Model
- Retrieval-Augmented Generation (RAG)

---

## 📂 Project Structure

```
RASHID-DENTAL-AI-ASSISTANT/

│
├── backend/
│ ├── main.py
│ ├── chatbot.py
│ ├── requirements.txt
│ ├── .env.example
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── knowledge_base/
│ ├── clinic.md
│ ├── services.md
│ ├── faq.md
│ ├── appointments.md
│ └── safety.md
│
├── README.md
└── .gitignore
```