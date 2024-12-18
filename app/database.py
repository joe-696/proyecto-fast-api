from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base de datos (asegúrate de que sea válida)
DATABASE_URL = "postgresql+asyncpg://fastapi_user:password@127.0.0.1/fastapi_db"

# Motor de base de datos asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Sesión asíncrona
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base para los modelos
Base = declarative_base()


# Dependencia para obtener una sesión de base de datos
async def get_db():
    async with SessionLocal() as session:
        yield session
