import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai
from pydantic import BaseModel

load_dotenv()

router = APIRouter()

# Initialize Gemini Client safely
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


class ChatRequest(BaseModel):
    question: str
    context: str = ""


class ChatResponse(BaseModel):
    answer: str


def generate_answer(question: str, context: str) -> str:
    if not client:
        return "Error: GEMINI_API_KEY is missing from your .env file."

    prompt = f"""
You are the AI assistant for Rashid Dental Clinic.
Answer ONLY using the information provided in the context below.
If the answer is not present in the context, say:
"I couldn't find that information in the clinic knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        # Standard model string for the google-genai SDK
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        err_msg = str(e)
        print(f"Gemini API Error: {err_msg}")

        # If quota is exhausted or rate limited, provide a clear fallback instead of throwing an unhandled 500
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            return "Rashid Dental Assistant: The AI service is currently receiving high demand. Rashid Dental Clinic offers general dentistry, tooth extractions, cleanings, and emergency dental consultations. Please try again in a few moments!"

        return f"Service Notice: Unable to generate response ({err_msg})"


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        answer = generate_answer(request.question, request.context)
        return ChatResponse(answer=answer)
    except Exception as e:
        print(f"Chatbot Endpoint Error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )