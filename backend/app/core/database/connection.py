from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
from app.core.settings import Settings



engine = create_async_engine(Settings.PG_URL)
async_session = sessionmaker(engine, class_=AsyncSession)
