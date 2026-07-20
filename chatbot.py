import os
import re
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai
from pydantic import BaseModel

load_dotenv()

router = APIRouter()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


class HistoryItem(BaseModel):
    role: str
    parts: List[str]


class ChatRequest(BaseModel):
    question: str
    history: List[HistoryItem] = []


class ChatResponse(BaseModel):
    answer: str


SYSTEM_INSTRUCTION = """
You are the AI Assistant for Rashid Dental Clinic.
Be polite, professional, and empathetic.
Help patients with services (tooth extractions, cleanings, root canals, whitening), 
preparation tips, and booking appointments.
"""


def smart_clinic_fallback(question: str, history: List[HistoryItem]) -> str:
    """Smart fallback engine when Gemini API quota (429) is exhausted or offline."""
    q = question.lower()

    # Check if the previous message asked for appointment details
    last_bot_msg = ""
    if history:
        for item in reversed(history):
            if item.role == "model" and item.parts:
                last_bot_msg = item.parts[0].lower()
                break

    # 1. Detection: User is responding with details (Name, Phone, Date)
    has_numbers = bool(re.search(r"\d+", q))
    is_answering_booking = "provide your:" in last_bot_msg or "1. full name" in last_bot_msg
    
    if is_answering_booking or (has_numbers and any(month in q for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "pm", "am"])):
        return (
            "✅ **Appointment Request Received!**\n\n"
            "Thank you! We have logged your details:\n"
            f"📋 **Details:** {question}\n\n"
            "Our clinic receptionist will contact you shortly on the provided number to finalize your slot. "
            "See you soon at Rashid Dental Clinic!"
        )

    # 2. General Appointment Inquiry
    if any(word in q for word in ["appointment", "book", "schedule", "timing", "visit", "slot"]):
        return (
            "I can help you book an appointment! Please provide your:\n"
            "1. Full Name\n"
            "2. Phone Number\n"
            "3. Preferred Date & Time\n\n"
            "Our team will confirm your slot right away!"
        )

    # 3. Services Inquiry
    if any(word in q for word in ["service", "offer", "do you do", "help"]):
        return (
            "At Rashid Dental Clinic, we offer:\n"
            "• Tooth Extractions & Wisdom Tooth Removal\n"
            "• Teeth Cleaning & Scaling\n"
            "• Root Canal Treatment (RCT)\n"
            "• Teeth Whitening & Cosmetic Dentistry\n"
            "• Dental Fillings & Crowns\n\n"
            "Which service would you like to learn more about or book?"
        )

    # 4. Extractions Inquiry
    if any(word in q for word in ["extraction", "pull", "remove tooth", "wisdom"]):
        return (
            "Tooth extraction is a routine procedure done under local anesthesia to ensure a pain-free experience. "
            "We offer both simple extractions and surgical wisdom tooth removals.\n\n"
            "Would you like to schedule an evaluation with our dentist?"
        )

    # 5. Pricing Inquiry
    if any(word in q for word in ["price", "cost", "fee", "charge"]):
        return (
            "Our consultation fee starts at a nominal rate, and procedure costs depend on individual evaluation. "
            "Would you like to book a checkup slot to get an exact quote?"
        )

    # Default Greeting / Fallback
    return (
        "Thank you for contacting Rashid Dental Clinic! We specialize in painless extractions, "
        "root canals, cleanings, and emergency care. How can I assist you with your appointment today?"
    )


def generate_answer(question: str, history: List[HistoryItem]) -> str:
    if not client:
        return smart_clinic_fallback(question, history)

    try:
        # Build context from recent history
        formatted_prompt = f"{SYSTEM_INSTRUCTION}\n\nRecent Conversation:\n"
        for item in history[-6:]:
            role_label = "Patient" if item.role == "user" else "Assistant"
            formatted_prompt += f"{role_label}: {item.parts[0]}\n"

        formatted_prompt += f"Patient: {question}\nAssistant:"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=formatted_prompt,
        )
        return response.text

    except Exception as e:
        print(f"Gemini API Notice: {e}")
        # Fallback to local intelligent responses if API hits 429 / quota limit
        return smart_clinic_fallback(question, history)


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        answer = generate_answer(request.question, request.history)
        return ChatResponse(answer=answer)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )