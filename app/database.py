import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
# Настройка подключения к базе данных
DATABASE_URL = f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost/{os.getenv("POSTGRES_DB")}"  # Замените на свои данные

# Создание асинхронного движка для подключения к базе данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий для взаимодействия с базой данных
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Создание базового класса для всех моделей данных
Base = declarative_base()


async def init_db():
    """Инициализация базы данных: создание всех таблиц."""
    async with engine.begin() as conn:
        # Создание всех таблиц, определенных в моделях
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Функция для получения асинхронной сессии базы данных."""
    async with AsyncSessionLocal() as session:
        yield session  # Возвращает сессию для использования в зависимости FastAPI
