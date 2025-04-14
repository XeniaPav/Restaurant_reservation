from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # Импортируйте AsyncSession
from app.database import get_db
from app.schemas.table import TableCreate, Table
from app.services.table_service import create_table, get_tables, delete_table
import logging

logger = logging.getLogger(__name__)

table_router = APIRouter()

@table_router.post("/tables/", response_model=Table)
async def create_new_table(
    table_create: TableCreate, db: AsyncSession = Depends(get_db)
):
    logger.info("Creating new table")
    return await create_table(db=db, table_create=table_create)

@table_router.get("/tables/")
async def read_tables(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching tables...")
    return await get_tables(db=db)

@table_router.delete("/tables/{table_id}")
async def remove_table(table_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Removing table with id {table_id}")
    success = await delete_table(db=db, table_id=table_id)
    if not success:
        raise HTTPException(status_code=404, detail="Table not found")
    return {"message": "Table deleted successfully"}