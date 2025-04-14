from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.table import Table as TableModel
from app.schemas.table import TableCreate

async def create_table(db: AsyncSession, table_create: TableCreate):
    db_table = TableModel(
        name=table_create.name,
        seats=table_create.seats,
        location=table_create.location
    )
    db.add(db_table)
    await db.commit()  # Асинхронный коммит
    await db.refresh(db_table)  # Асинхронное обновление
    return db_table

async def get_tables(db: AsyncSession):
    result = await db.execute(select(TableModel))  # Асинхронный запрос
    return result.scalars().all()  # Получаем все результаты

async def delete_table(db: AsyncSession, table_id: int):
    result = await db.execute(select(TableModel).filter(TableModel.id == table_id))
    table = result.scalar_one_or_none()  # Получаем таблицу или None

    if table:
        await db.delete(table)  # Удаляем таблицу
        await db.commit()  # Коммитим изменения
        return True
    return False  # Если таблица не найдена, возвращаем False