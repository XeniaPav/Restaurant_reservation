from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from fastapi import HTTPException
from datetime import timedelta
import logging
from app.models.reservation import Reservation as ReservationModel
from app.models.table import Table as TableModel
from app.schemas.reservation import ReservationCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_reservation(db: AsyncSession, reservation_create: ReservationCreate):
    """Создание бронирования"""
    try:
        # Проверка на существование столика
        table_exists = await db.execute(
            select(TableModel).filter(TableModel.id == reservation_create.table_id)
        )

        if table_exists.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Столик не найден.")

        # Проверка на пересечение временных слотов
        existing_reservations = await db.execute(
            select(ReservationModel).filter(
                and_(
                    ReservationModel.table_id == reservation_create.table_id,
                    ReservationModel.reservation_time
                    < (
                        reservation_create.reservation_time
                        + timedelta(minutes=reservation_create.duration_minutes)
                    ),
                    (
                        ReservationModel.reservation_time
                        + timedelta(minutes=reservation_create.duration_minutes)
                    )
                    > reservation_create.reservation_time,
                )
            )
        )

        if existing_reservations.scalars().first() is not None:
            raise HTTPException(
                status_code=400,
                detail="Столик уже зарезервирован на выбранный временной интервал.",
            )

        # Создание нового бронирования
        db_reservation = ReservationModel(
            customer_name=reservation_create.customer_name,
            table_id=reservation_create.table_id,
            reservation_time=reservation_create.reservation_time,
            duration_minutes=reservation_create.duration_minutes,
        )

        db.add(db_reservation)
        await db.commit()
        await db.refresh(db_reservation)
        return db_reservation

    except HTTPException as http_exc:
        raise http_exc  # Перебрасываем HTTP исключение


async def get_reservations(db: AsyncSession):
    """Список бронирований"""
    try:
        result = await db.execute(select(ReservationModel))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error fetching reservations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_reservation(db: AsyncSession, reservation_id: int):
    """Удаление бронирования"""
    try:
        result = await db.execute(
            select(ReservationModel).filter(ReservationModel.id == reservation_id)
        )
        reservation = result.scalar_one_or_none()

        if reservation:
            await db.delete(reservation)
            await db.commit()
            logger.info("Бронирование отменено")
            return {"detail": "Бронирование отменено"}

        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error deleting reservation with id {reservation_id}: {str(e)}")
