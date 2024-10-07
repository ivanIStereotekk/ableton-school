from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from settings import *
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.models import Base,User


## database URL
DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

# Engine which invokes connection to DB
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """Create database and tables : Async function
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get AsyncSession: Async functon:
    Returns:
        AsyncGenerator[AsyncSession, None]:
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get user database: Async function
    Args:
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).

    Yields:
        _type_: User
    """
    yield SQLAlchemyUserDatabase(session, User)


