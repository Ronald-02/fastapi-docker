from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

# Criação do engine assíncrono
async_engine = create_async_engine(DATABASE_URL, echo=True)

engine = create_async_engine(DATABASE_URL, echo = True)

# Session assíncrona
SessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para modelos
Base = declarative_base()

# Função para injetar sessão no FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
