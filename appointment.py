from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AppointmentRequest(BaseModel):
    name: str
    phone: str
    preferred_date: str
    message: str

appointments = []

@router.post("/appointment")
def book_appointment(data: AppointmentRequest):
    appointments.append(data.dict())

    return {
        "message": "Your appointment request has been received.",
        "status": "success"
    }