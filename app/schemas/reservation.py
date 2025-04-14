from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    """Схема созания брони столика"""

    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int


class Reservation(ReservationCreate):
    """Схема брони столика"""

    id: int

    class Config:
        from_attributes = True
