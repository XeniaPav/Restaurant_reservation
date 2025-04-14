from pydantic import BaseModel


class TableCreate(BaseModel):
    """Схема создания столика"""

    name: str
    seats: int
    location: str


class Table(TableCreate):
    """Схема столика"""

    id: int

    class Config:
        from_attributes = True
