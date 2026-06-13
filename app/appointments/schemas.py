from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class AppointmentCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    owner_id: int


class Appointment(AppointmentCreate):
    id: int


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
