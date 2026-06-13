

from sqlalchemy import create_engine,engine
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,AsyncSession
from src.utils.settings import settings

engine = create_async_engine(settings.DATABASE_URL)
DB_Session = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

DBModel=declarative_base()


async def get_db():
    async with DB_Session() as session:
        yield session
    
