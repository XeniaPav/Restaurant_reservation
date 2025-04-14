from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.table import Table as TableModel
from app.schemas.table import TableCreate


async def create_table(db: AsyncSession, table_create: TableCreate):
    db_table = TableModel(
        name=table_create.name, seats=table_create.seats, location=table_create.location
    )
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table


async def get_tables(db: AsyncSession):
    result = await db.execute(select(TableModel))
    return result.scalars().all()


async def delete_table(db: AsyncSession, table_id: int):
    result = await db.execute(select(TableModel).filter(TableModel.id == table_id))
    table = result.scalar_one_or_none()
    if table:
        await db.delete(table)
        await db.commit()
        return True
    return False
