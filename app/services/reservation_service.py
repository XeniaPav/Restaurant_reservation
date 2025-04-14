from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.reservation import Reservation as ReservationModel
from app.schemas.reservation import ReservationCreate

async def create_reservation(db: AsyncSession, reservation_create: ReservationCreate):
    try:
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
    except Exception as e:
        logger.error(f"Error creating reservation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def get_reservations(db: AsyncSession):
    try:
        result = await db.execute(select(ReservationModel))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error fetching reservations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def delete_reservation(db: AsyncSession, reservation_id: int):
    try:
        result = await db.execute(select(ReservationModel).filter(ReservationModel.id == reservation_id))
        reservation = result.scalar_one_or_none()

        if reservation:
            await db.delete(reservation)
            await db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting reservation with id {reservation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")