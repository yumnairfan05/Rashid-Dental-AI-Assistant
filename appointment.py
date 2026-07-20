from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AppointmentRequest(BaseModel):
    patient_name: str
    phone: str
    date: str


@router.post("/appointment")
def book_appointment(req: AppointmentRequest):
    return {
        "status": "Success",
        "message": f"Appointment booked for {req.patient_name} on {req.date}",
    }