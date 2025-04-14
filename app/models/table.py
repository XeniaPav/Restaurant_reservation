from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Table(Base):
    """Модель столика"""

    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    seats = Column(Integer)
    location = Column(String)
