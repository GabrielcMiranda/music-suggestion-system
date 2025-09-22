from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

PG_URL = getenv('PG_URL')

engine = create_async_engine(PG_URL)
async_session = sessionmaker(engine, class_=AsyncSession)
