from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.reservation import ReservationCreate, Reservation
from app.services.reservation_service import (
    create_reservation,
    get_reservations,
    delete_reservation,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
reservation_router = APIRouter()


@reservation_router.post("/reservations/", response_model=Reservation)
async def create_new_reservation(
    reservation_create: ReservationCreate, db: AsyncSession = Depends(get_db)
):
    logger.info("Creating new reservation")
    return await create_reservation(db=db, reservation_create=reservation_create)


@reservation_router.get("/reservations/")
async def read_reservations(db: AsyncSession = Depends(get_db)):
    logger.info("Reading reservations")
    return await get_reservations(db=db)


@reservation_router.delete("/reservations/{reservation_id}")
async def remove_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    logger.info("Removing reservation")
    success = await delete_reservation(db=db, reservation_id=reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return {"message": "Бронирование удалено"}
