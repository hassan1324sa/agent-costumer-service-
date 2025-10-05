from pydantic import BaseModel
from datetime import datetime

class Booking(BaseModel):
    username: str
    service_type: str  # "course" / "doctor" / "meeting" /
    date: str
    time: str
    created_at: datetime
