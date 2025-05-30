import uvicorn
from fastapi import FastAPI
from app.routers.table_router import table_router
from app.routers.reservation_router import reservation_router
from app.database import init_db
import logging
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

# Подключение маршрутов
app.include_router(table_router)
app.include_router(reservation_router)


@app.get("/")
async def read_root():
    logger.info("Root endpoint was called")
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    logger.info("Initializing the database...")
    asyncio.run(init_db())
    logger.info("Starting the server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)

