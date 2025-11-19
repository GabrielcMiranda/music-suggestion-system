from asyncio import run

from app.core.database.connection import engine
from app.models import Base
import logging

async def create_database():
    """Cria as tabelas apenas se elas não existirem"""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    run(create_database())
    logging.info("Database initialized!")
    print('Database initialized!')