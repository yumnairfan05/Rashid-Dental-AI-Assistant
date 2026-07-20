from appointment import router as appointment_router
from chatbot import router as chatbot_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI(title="Rashid Dental AI Assistant")

# Add CORS Middleware so frontend can send requests seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(chatbot_router)
app.include_router(appointment_router)


# Root check endpoint
@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Rashid Dental AI Assistant Backend is Running",
    }