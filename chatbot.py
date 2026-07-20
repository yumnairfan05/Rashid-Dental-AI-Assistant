import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question, context):
    prompt = f"""
You are the AI assistant for Rashid Dental Clinic.

Answer ONLY using the information below.

If the answer is not present in the context, say:
"I couldn't find that information in the clinic knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text