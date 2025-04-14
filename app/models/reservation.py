from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.models.table import Base

class Reservation(Base):
    """Модель брони"""

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    table_id = Column(Integer, ForeignKey("tables.id"))
    reservation_time = Column(DateTime)
    duration_minutes = Column(Integer)
