from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from DataBase.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def async_main():
    from DataBase.models.users import User
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)